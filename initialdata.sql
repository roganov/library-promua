BEGIN TRANSACTION;
INSERT INTO "alembic_version" VALUES('48d6a3fff8f1');
INSERT INTO "book" VALUES(1,'Harry Potter and the Philosopher''s Stone');
INSERT INTO "book" VALUES(5,'American Sniper');
INSERT INTO "book" VALUES(6,'Speak, Memory');
INSERT INTO "book" VALUES(7,'The Elements of Statistical Learning: Data Mining, Inference, and Prediction');
INSERT INTO "book" VALUES(8,'On the Road');
INSERT INTO "book" VALUES(9,'Visions of Cody');
INSERT INTO "book" VALUES(10,'Doctor Sax');
INSERT INTO "book" VALUES(11,'Design Patterns: Elements of Reusable Object-Oriented Software');
INSERT INTO "book" VALUES(12,'Harry Potter and the Deathly Hallows');
INSERT INTO "book" VALUES(13,'The Silkworm');
INSERT INTO "user" VALUES(2,'user@mail.com','pbkdf2:sha1:1000$1gH1snPA$3dbc3b11706639f12896fa9bed1df2e08f83b818',0);
INSERT INTO "user" VALUES(3,'superuser@mail.com','pbkdf2:sha1:1000$k4ZKbnjN$10adcfa7a1c5c745d4e64c781606a8657526ab48',1);
INSERT INTO "author" VALUES(1,'Joanne Rowling');
INSERT INTO "author" VALUES(9,'Chris Kyle');
INSERT INTO "author" VALUES(11,'Vladimir Nabokov');
INSERT INTO "author" VALUES(12,'Jerome H. Friedman');
INSERT INTO "author" VALUES(13,'Robert Tibshirani');
INSERT INTO "author" VALUES(14,'Trevor Hastie');
INSERT INTO "author" VALUES(15,'Jack Kerouac');
INSERT INTO "author" VALUES(16,'Erich Gamma');
INSERT INTO "author" VALUES(17,'John Vlissides');
INSERT INTO "author" VALUES(18,'Ralph Johnson');
INSERT INTO "author" VALUES(19,'Richard Helm');
INSERT INTO "book_author" VALUES(1,1);
INSERT INTO "book_author" VALUES(5,9);
INSERT INTO "book_author" VALUES(6,11);
INSERT INTO "book_author" VALUES(7,12);
INSERT INTO "book_author" VALUES(7,13);
INSERT INTO "book_author" VALUES(7,14);
INSERT INTO "book_author" VALUES(8,15);
INSERT INTO "book_author" VALUES(9,15);
INSERT INTO "book_author" VALUES(10,15);
INSERT INTO "book_author" VALUES(11,16);
INSERT INTO "book_author" VALUES(11,17);
INSERT INTO "book_author" VALUES(11,18);
INSERT INTO "book_author" VALUES(11,19);
INSERT INTO "book_author" VALUES(12,1);
INSERT INTO "book_author" VALUES(13,1);
COMMIT;