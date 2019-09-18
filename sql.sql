show tables;

select * from u_user;
select * from u_group;
select * from u_user_group;
select * from u_permission;
select * from u_user_permission;


CREATE TABLE u_user(
    id INT auto_increment PRIMARY KEY COMMENT '用户表id',
    email VARCHAR(64) NOT NULL COMMENT 'email地址',
    phone VARCHAR(16) NOT NULL DEFAULT '' COMMENT '手机',
    username VARCHAR(64) NOT NULL DEFAULT '' COMMENT '用户名,默认为邮箱前缀',
    password_hash VARCHAR(256) NOT NULL COMMENT '用户密码',
    role_id tinyint NOT NULL DEFAULT 3 COMMENT '用户角色id, 1:admin 2:leader, 3:staff',
    status tinyint NOT NULL default 0 COMMENT '用户账号状态, 0:未激活, 1:激活',
    join_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建账号时间',
    UNIQUE KEY email(email),
    KEY join_time(join_time)
    )engine=Innodb charset=utf8 COMMENT '用户表';


CREATE TABLE u_group(
id int auto_increment PRIMARY KEY COMMENT '产品组id',
code VARCHAR(64) NOT NULL COMMENT '组code',
name VARCHAR(64) NOT NULL COMMENT '组name',
UNIQUE KEY codename(code, name)
)engine=Innodb charset=utf8 COMMENT '用户组表';

drop table u_user_group;
CREATE TABLE u_user_group(
id INT auto_increment PRIMARY KEY COMMENT '主键id',
uid INT NOT NULL COMMENT '关联的用户id',
gid INT NOT NULL COMMENT '关联的组id',
UNIQUE KEY ugid(uid, gid)
)engine=Innodb charset=utf8 COMMENT '用户所属组别表';


CREATE TABLE u_permission(
id INT auto_increment PRIMARY KEY COMMENT '主键id',
code VARCHAR(64) NOT NULL COMMENT '权限码',
name VARCHAR(64) NOT NULL COMMENT '权限名',
content_type VARCHAR(256) NOT NULL DEFAULT '' COMMENT '权限对应的资源',
UNIQUE KEY code(code)
)engine=Innodb charset=utf8 COMMENT '权限表';


CREATE TABLE u_user_permission(
id INT auto_increment PRIMARY KEY COMMENT '主键id',
uid INT NOT NULL COMMENT '关联的用户id',
pid INT NOT NULL COMMENT '关联的权限id',
UNIQUE KEY upid(uid, pid)
)engine=Innodb charset=utf8 COMMENT '用户权限表';

