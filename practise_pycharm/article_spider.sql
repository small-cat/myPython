CREATE TABLE article (
    title varchar(200) NOT NULL,
    create_date date,
    url varchar(300) NOT NULL, 
    url_object_id varchar(50) NOT NULL PRIMARY KEY, 
    front_img_url varchar(300), 
    front_img_path varchar(200), 
    comment_nums int(11) NOT NULL DEFAULT 0, 
    fav_nums int(11) NOT NULL DEFAULT 0, 
    vote_nums int(11) NOT NULL DEFAULT 0, 
    tags varchar(200), 
    content longtext NOT NULL
)ENGINE=InnoDB default charset=utf8;
