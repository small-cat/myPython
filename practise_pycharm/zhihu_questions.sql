create table zhihu_answer (
    zhihu_id bigint(20) NOT NULL PRIMARY KEY, -- 问题的ID，是唯一的
    url varchar(200) NOT NULL, -- 问题的 url
    question_id bigint(20) NOT NULL, -- 每一个回答都有一个 ID  
    author_id varchar(100), 
    author_name varchar(100), 
    author_gender int(1), 
    content longtext NOT NULL, 
    praise_num int(11) NOT NULL default 0, -- 问题回答的点赞数
    comments_num int(11) NOT NULL default 0, -- 问题回答的评论数
    create_time date NOT NULL, 
    update_time date NOT NULL, 
    crawl_time datetime NOT NULL, -- 爬取的时间，会反复爬取，爬取所有回答
    crawl_update_time date
)Engine=InnoDB default character set utf-8;

create table zhihu_question (
    zhihu_id bigint(20) NOT NULL PRIMARY KEY, 
    question_url varchar(200) NOT NULL, 
    question_title longtext NOT NULL, 
    answer_num int(11), 
    comments_num int(11) NOT NULL default 0, 
    attentioned_num int(11), -- 关注数
    scanned_num int(11),     -- 浏览数
    tags varchar(200)
)Engine=InnoDB default character set utf-8;


