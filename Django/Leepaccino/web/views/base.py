# -*- coding: utf-8 -*-

from django.views import View
from django.http import (
    Http404,
    JsonResponse
)
from django.shortcuts import render
from passlib.hash import bcrypt
from hashlib import sha1

from Leepaccino.settings import SECRET_KEY
from . import User
from ..utils.exception import ArgumentNullException
from ..utils.helper import ObjectDict


_INVALID_OBJECT = object()


class BaseView(View):
    """BaseView"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._site = None
        self._client = None
        self._token = None
        self._language = None

    def dispatch(self, request, *args, **kwargs):
        # ==================================================
        # ----------- Request Headers Set ------------------
        self._prepare(request)
        self.get_user(request, token=self._token)
        return super().dispatch(request, *args, **kwargs)
        # --------------------------------------------------
        # ==================================================

    def _prepare(self, request):
        # Some Prepare Work
        self._site = request.META.get('HTTP_SITE')
        self._client = request.META.get('HTTP_CLIENT')
        self._token = request.META.get('HTTP_TOKEN')
        self._language = request.META.get('HTTP_LANGUAGE')

    @staticmethod
    def _gen_token(token_db, secret_key=SECRET_KEY):
        # generate token
        secret_key_hash = sha1(secret_key.encode()).hexdigest()
        prefix = secret_key_hash[12:16]
        suffix = secret_key_hash[16:20]
        label = '$2b$12$'
        mid = token_db.split(label)[1]
        return prefix + '.' + mid + suffix

    def get_user(self, request, *, email=None, password=None, token=None):
        user, user_info = None, None
        # auth with token
        if token:
            label = '$2b$12$'
            token_suffix = token[5:]
            token_db = label + token_suffix[:-4]
            user = User.objects.filter(token=token_db).first()
        # auth with email + password
        if all([not user, email, password]):
            user_exists = User.objects.filter(email=email).first()
            if user_exists:
                if bcrypt.verify(password, user_exists.token):
                    user = user_exists
                    token = self._gen_token(user.token)
        if user:
            user_info = ObjectDict(
                dict(id=user.id,
                     email=user.email,
                     token=token,
                     username=user.username,
                     realname=user.realname,
                     birthday=user.birthday))
        request.user = user_info
        return user_info

    @property
    def headers(self):
        return dict(
            Site=self._site,
            Client=self._client,
            Token=self._token,
            Language=self._language)

    @property
    def _out_headers(self):
        # Response Output Header
        return dict(
            Site=self._site,
            Client=self._client,
            Token=self._token,
            Language=self._language)

    def get(self, request):
        # Subclass Rewrite
        raise Http404()

    def post(self, request):
        # Subclass Rewrite
        raise Http404()

    def render_html(self, html, *args, **kwargs):
        return render(self.request, html, *args, **kwargs)

    def get_argument(self, query_param, default=_INVALID_OBJECT):
        # 从query_string/body中获取参数
        # 若没有提供参数，返回默认值default
        # 若没有提供默认值，参数为空时引发异常
        if query_param in self.request.GET:
            return self.request.GET[query_param]
        elif query_param in self.request.POST:
            return self.request.POST[query_param]
        elif default is _INVALID_OBJECT:
            raise ArgumentNullException(
                'Argument `{}` must not be null'.format(query_param))
        else:
            return default

    def get_arguments(self, query_params, default=_INVALID_OBJECT, *, result_type=None,):
        # 从query_string/body中获取多个参数
        # 若没有提供参数，返回默认值default
        # 若没有提供默认值, 其中一个参数为空时引发异常
        # 返回dict指定result_type为dict
        def get_args(x):
            return self.get_argument(x, default)
        result = list(map(get_args, query_params))
        if _INVALID_OBJECT in result:
            raise ArgumentNullException(
                'Argument `{}` must not be null'.format(query_params))
        if result_type is dict:
            return dict(zip(query_params, result))
        return result


class BaseHandler(BaseView):

    def render_json(self, data=None, *, code='0', msg='ok', chunk=None, **kwargs):
        #  Json Response Render
        if isinstance(chunk, dict) and {'code', 'data', 'msg'}.issubset(chunk):
            response = chunk
        else:
            response = dict(code=code, msg=msg, data=data)
        response = JsonResponse(response)
        # =====================================================================
        # ----------------------- Response Headers Set ------------------------
        for k, v in self._out_headers.items():
            response[k] = v
        for k, v in kwargs.items():
            response[k] = v
        return response
        # ---------------------------------------------------------------------
        # =====================================================================
