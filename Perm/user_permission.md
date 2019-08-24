[toc]

* /api/vi/user/login 用户登录
* /api/vi/user/login 用户退出、
* /api/vi/check_user_exists 查看email是否已经存在
* /api/vi/user/add_user 添加用户
* /api/vi/user/info 用户信息获取
* /api/vi/user/info 用户信息更新


### POST /api/vi/user/login 用户登录

#### POST 参数
| 参数名    |  类型   | 是否必须 | 说明         | 示例                    |
| -------- | ------ | ------- | ----------- | ---------------------- |
| name     | string | 是      | 用户名/邮箱名  | admin@sinaif.com       |
| password | string | 是      | 用户密码      | password123            |


#### 返回参数
| 参数名       |  类型   | 说明                           |
| ----------- | ------ | ----------------------------- |
| status      | int    | 账号是否激活 1: 激活, 0: 未激活   |
| token       | string | token                         |
| username    | string | 用户名                         |
| id          | int    | 用户id                         |
| role_id     | int    | 用户角色id                      |
| email       | string | 用户邮箱                        |
| groups      | List   | 用户所属组信息                    |
| permissions | Dict   | 用户权限信息                     |


#### groups 参数
| 参数名    |  类型   | 说明         |
| -------- | ------ | ------------ |
| id       | int    | 组id         |
| code     | string | 组code       |
| name     | string | 组name       |


#### permissions 参数
| 参数名        |  类型   | 说明                 |
| ------------ | ------ | -------------------- |
| id           | int    | 权限id                |
| code         | string | 权限code              |
| name         | string | 权限name              |
| content_type | string | 权限控制的资源          |


#### 示例
```
{
    "code": 200,
    "msg": "ok",
    "data": {
        "status": 1,
        "token": "$pbkdf2-sha256$29000$QOhdq/V.z1nLmdO6935vrQ$ozejguFlHSWv/E7EROh9njas3kFRmJkk/WmTu5Aa2Wo",
        "username": "Admin",
        "id": 1,
        "role_id": 1,
        "email": "admin@sinaif.com",
        "groups": [
            {
                "code": "D1001",
                "id": 1,
                "name": "新浪卡贷"
            },
            {
                "code": "D1002",
                "id": 2,
                "name": "新浪有借"
            },
            {
                "code": "D1003",
                "id": 3,
                "name": "熊猫贷款"
            },
            {
                "code": "D1004",
                "id": 4,
                "name": "大王贷款"
            }
        ],
        "permissions": {
            "测试权限": [
                {
                    "id": 1,
                    "name": "获取",
                    "content_type": " ",
                    "code": "ces_add"
                },
                {
                    "id": 2,
                    "name": "更新",
                    "content_type": " ",
                    "code": "ces_update"
                },
                {
                    "id": 3,
                    "name": "删除",
                    "content_type": " ",
                    "code": "ces_delete"
                }
            ],
            "测试权限1": [
                {
                    "id": 4,
                    "name": "获取",
                    "content_type": " ",
                    "code": "ces1_add"
                },
                {
                    "id": 5,
                    "name": "更新",
                    "content_type": " ",
                    "code": "ces1_update"
                },
                {
                    "id": 6,
                    "name": "删除",
                    "content_type": " ",
                    "code": "ces1_delete"
                }
            ]
        }
    }
}
```



### GET /api/vi/user/logout 用户退出

#### GET 参数
无

#### 返回参数


#### 示例
```
{
    "code": 200,
    "msg": "ok",
    "data": {
        "result": 1
        }
}
```



### GET /api/vi/check_user_exists 查看email是否已经存在

#### GET 参数
| 参数名       |  类型   | 是否必须 | 说明                | 示例                    |
| ----------- | ------ | ------- | ------------------ | ---------------------- |
| email       | string | 是      | 用户名/邮箱名         | "admin@sinaif.com"       |


#### 返回参数
result为1表示邮箱已经注册, 为0表示未注册


#### 示例
```
{
    "code": 200,
    "msg": "ok",
    "data": {
        "result": 1
        }
}
```



### POST /api/vi/user/add_user 添加用户

#### POST 参数
| 参数名       |  类型   | 是否必须 | 说明                | 示例                    |
| ----------- | ------ | ------- | ------------------ | ---------------------- |
| email       | string | 是      | 用户名/邮箱名         | "admin@sinaif.com"       |
| username    | string | 是      | 用户密码              | "Admin"                  |
| password    | string | 是      | 用户密码              | "password123"            |
| role_id     | int    | 否      | 用户角色id, 1:admin 2:leader 3:staff  | 2                 |
| groups      | string | 否      | 用户组id, 多个用逗号分开 | "1,2,3"                 |
| permissions | string | 否      | 权限id, 多个用逗号分开  | "1,2,3"                  |

#### 返回参数


#### 示例
```
{
    "code": 200,
    "msg": "ok",
    "data": {
        "email": "test49@sinaif.com",
        "username": "Test",
        "password_hash": "$pbkdf2-sha256$29000$ZYwxRqg15nyP8f7fO4eQsg$r90sZ7X6svxMfMWLOuVwACVAIxtIEET3Zx6/HRpb1kw",
        "id": 20,
        "role_id": 3,
        "status": 0,
        "groups": [
            {
                "code": "D1001",
                "id": 1,
                "name": "新浪卡贷"
            },
            {
                "code": "D1002",
                "id": 2,
                "name": "熊猫贷款"
            },
            {
                "code": "D1003",
                "id": 3,
                "name": "新浪有借"
            },
            {
                "code": "D1004",
                "id": 4,
                "name": "商业化"
            }
        ],
        "permissions": {
            "权限测试": [
                {
                    "id": 1,
                    "name": "新建",
                    "content_type": " ",
                    "code": "ces_add"
                },
                {
                    "id": 2,
                    "name": "更新",
                    "content_type": " ",
                    "code": "ces_update"
                },
                {
                    "id": 3,
                    "name": "删除",
                    "content_type": " ",
                    "code": "ces_delete"
                }
            ]
        }
    }
}
```




### GET /api/vi/user/info 用户信息获取

#### GET 参数
| 参数名       |  类型   | 是否必须 | 说明                | 示例                    |
| ----------- | ------ | ------- | ------------------ | ---------------------- |
| email       | string | 否      | 用户名/邮箱名, 不提供则返回所有用户, 多个用逗号分开 | "admin@sinaif.com,leo@sinaif.com"       |

#### 返回参数


#### 示例
```
{
    "code": "0",
    "msg": "ok",
    "data": [
        {
            "status": 1,
            "password_hash": "$pbkdf2-sha256$29000$QOhdq/V.z1nLmdO6935vrQ$ozejguFlHSWv/E7EROh9njas3kFRmJkk/WmTu5Aa2Wo",
            "username": "Admin",
            "id": 1,
            "role_id": 1,
            "email": "admin@sinaif.com",
            "groups": [
                {
                    "code": "D1001",
                    "id": 1,
                    "name": "新浪卡贷"
                },
                {
                    "code": "D1002",
                    "id": 2,
                    "name": "新浪有借"
                },
                {
                    "code": "D1003",
                    "id": 3,
                    "name": "熊猫贷款"
                },
                {
                    "code": "D1004",
                    "id": 4,
                    "name": "大王贷款"
                }
            ],
            "permissions": {
                "测试权限": [
                    {
                        "id": 1,
                        "name": "获取",
                        "content_type": " ",
                        "code": "ces_add"
                    },
                    {
                        "id": 2,
                        "name": "更新",
                        "content_type": " ",
                        "code": "ces_update"
                    },
                    {
                        "id": 3,
                        "name": "删除",
                        "content_type": " ",
                        "code": "ces_delete"
                    }
                ],
                "测试权限1": [
                    {
                        "id": 4,
                        "name": "获取",
                        "content_type": " ",
                        "code": "ces1_add"
                    },
                    {
                        "id": 5,
                        "name": "更新",
                        "content_type": " ",
                        "code": "ces1_update"
                    },
                    {
                        "id": 6,
                        "name": "删除",
                        "content_type": " ",
                        "code": "ces1_delete"
                    }
                ]
            }
        },
        {
            "status": 1,
            "password_hash": "$pbkdf2-sha256$29000$DiEEoNRaa611bm1N6f3/Pw$wID6IZ0JtwoWM6swaFcTGLzp8dNVYk085KQZJftN60w",
            "username": "Leo",
            "id": 2,
            "role_id": 3,
            "email": "leo@sinaif.com",
            "groups": [
                {
                    "code": "D1002",
                    "id": 2,
                    "name": "新浪有借"
                }
            ],
            "permissions": {}
        }
    ]
}
```



### POST /api/vi/user/info 用户信息更新

#### POST 参数
| 参数名       |  类型   | 是否必须 | 说明                | 示例                    |
| ----------- | ------ | ------- | ------------------ | ---------------------- |
| email       | string | 是      | 用户名/邮箱名         | "admin@sinaif.com"     |
| username    | string | 否      | 用户密码              | "Admin"                |
| password    | string | 否      | 用户密码              | "password123"          |
| role_id     | int    | 否      | 用户角色1:admin 2:leader 3:staff|   2          |
| status      | int    | 否      | 用户账户状态1:激活 2:关闭| 1                     |
| groups      | string | 否      | 用户组id, 多个用逗号分开 | "1,2,3"               |
| permissions | string | 否      | 权限id, 多个用逗号分开  | "1,2,3"                |

#### 返回参数


#### 示例
```
{
    "code": 200,
    "msg": "ok",
    "data": {
        "status": 1,
        "password_hash": "$pbkdf2-sha256$29000$DiEEoNRaa611bm1N6f3/Pw$wID6IZ0JtwoWM6swaFcTGLzp8dNVYk085KQZJftN60w",
        "username": "Leo",
        "id": 2,
        "role_id": 1,
        "email": "leo@sinaif.com",
        "groups": [
            {
                "code": "D1001",
                "id": 1,
                "name": "新浪卡贷"
            },
            {
                "code": "D1002",
                "id": 2,
                "name": "新浪有借"
            },
            {
                "code": "D1003",
                "id": 3,
                "name": "熊猫贷款"
            },
            {
                "code": "D1004",
                "id": 4,
                "name": "大王贷款"
            }
        ],
        "permissions": {
            "测试权限": [
                {
                    "id": 1,
                    "name": "获取",
                    "content_type": " ",
                    "code": "ces_add"
                },
                {
                    "id": 2,
                    "name": "更新",
                    "content_type": " ",
                    "code": "ces_update"
                },
                {
                    "id": 3,
                    "name": "删除",
                    "content_type": " ",
                    "code": "ces_delete"
                }
            ],
            "测试权限1": [
                {
                    "id": 4,
                    "name": "获取",
                    "content_type": " ",
                    "code": "ces1_add"
                },
                {
                    "id": 5,
                    "name": "更新",
                    "content_type": " ",
                    "code": "ces1_update"
                },
                {
                    "id": 6,
                    "name": "删除",
                    "content_type": " ",
                    "code": "ces1_delete"
                }
            ]
        }
    }
}
```


