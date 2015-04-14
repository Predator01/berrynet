create view lonely_words as 
select id_word from word_count where count = 1 group by id_word;
select * from lonely_words;

select count(*) from word_conditional_probability;
select count(*) from word_conditional_probability where id_word in lonely_words;
delete from word_conditional_probability where id_word in lonely_words;

select count(*) from word_category;
select count(*) from word_category where id_word in lonely_words;
delete from word_category where id_word in lonely_words;

select count(*) from word_count;
select count(*) from word_count where id_word in lonely_words;
delete from word_count where id_word in lonely_words;

select count(*) from word where word.id not in (select id_word from word_count group by id_word);
delete from word where id not in (select id_word from word_count group by id_word);
