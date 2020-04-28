-- 帖子表
drop table if exists article ;
create table article (
  id integer auto_increment primary key ,
  acticle_id varchar(64) not null ,
  acticle_title varchar(64),
  acticle_views varchar(32),
  acticle_replies varchar(32),
  acticle_authorid varchar(32),
  acticle_grouptitle varchar(128),
  acticle_content_type int ,
  louzhuid varchar(32) comment '发帖人的id',
  louzhu int not null comment '1, 楼主 是否是楼主',
  postcount varchar(32),
  index(acticle_id, louzhuid)
)default charset='utf8' ;

-- 评论表
drop table if exists comments;
create table comments (
  id integer auto_increment primary key ,
  acticle_id varchar(64) not null comment '评论的是哪篇帖子',
  comment_pid varchar(64) comment '评论的 pid',
  comment_name varchar(32) comment '评论者名称',
  comment_time date comment '评论时间',
  comment_content varchar(32) comment '评论内容',
  index(acticle_id)
)default charset='utf8';

-- 用户表
drop table if exists users;
create table users (
  id integer auto_increment primary key ,
  user_id varchar(64) not null ,
  user_brief varchar(64) comment '用户简介',
  user_address varchar(32) comment '所在地',
  user_gender int comment '1 男 2 女 0 未知',
  register_at date comment '注册时间',
  name varchar(32) ,
  avatar_img varchar(64) comment '头像url',
--   pet_name varchar(32) comment '宠物名',
--   pet_type varchar(32) comment '宠物品种',
  like_count varchar(32) comment '用户点赞数',
  reply_count varchar(32) comment '用户获得评论数',
  fans_count varchar(32) comment '粉丝数',
  follow_count varchar(32) comment '关注数',
  postcount varchar(32) comment '发帖数',
  index(user_id)
)default charset='utf8' ;