create database if not exists spider default character set = 'utf8';
create table if not exists spider.datas
(
    _id      int auto_increment,
    content  text         not null,
    author   varchar(20)  not null,
    title    varchar(160)  not null,
    news_url varchar(100) not null
        primary key,
    times    varchar(80)  not null,
    shenHe   varchar(60)  not null,
    click    int          not null,
    constraint datas__id_uindex
        unique (_id),
    constraint datas_news_url_uindex
        unique (news_url)
);

