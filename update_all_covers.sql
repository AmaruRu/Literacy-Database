-- SQL Script to Update All Book Cover URLs
-- Generated from Book_Recs.xls

USE MS_DBMS;

-- Check current book count
SELECT COUNT(*) as total_books FROM books;

-- Update book cover URLs
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/81aeV2igJsL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Biscuit Goes to School' AND author = 'Alyssa Satin Capucilli' AND grade_level = 'Kindergarten';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/61gYTpPyCDL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Biscuit Finds a Friend' AND author = 'Alyssa Satin Capucilli' AND grade_level = 'Kindergarten';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/91iqwEk-7kL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Biscuit\'s Day at the Farm' AND author = 'Alyssa Satin Capucilli' AND grade_level = 'Kindergarten';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780060741723_p0_v1_s1200x630.jpg' 
WHERE title = 'Biscuit and the Little Pup' AND author = 'Alyssa Satin Capucilli' AND grade_level = 'Kindergarten';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/51Q8GeKqypL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Biscuit and the Lost Teddy Bear' AND author = 'Alyssa Satin Capucilli' AND grade_level = 'Kindergarten';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780064442121_p0_v6_s1200x630.jpg' 
WHERE title = 'Biscuit' AND author = 'Alyssa Satin Capucilli' AND grade_level = 'Kindergarten';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/71Jfbjvm+dL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Biscuit in the Garden' AND author = 'Alyssa Satin Capucilli' AND grade_level = 'Kindergarten';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/91I1IXX1GaL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Biscuit\'s Big Friend' AND author = 'Alyssa Satin Capucilli' AND grade_level = 'Kindergarten';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780061177491_p0_v1_s600x595.jpg' 
WHERE title = 'Biscuit Meets the Class Pet' AND author = 'Alyssa Satin Capucilli' AND grade_level = 'Kindergarten';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780060094614_p0_v1_s1200x630.jpg' 
WHERE title = 'Biscuit and the Baby' AND author = 'Alyssa Satin Capucilli' AND grade_level = 'Kindergarten';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/81+qKRvpqaL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Biscuit Visits the Big City' AND author = 'Alyssa Satin Capucilli' AND grade_level = 'Kindergarten';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/7157CblHHcL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Don\'t Let The Pigeon Drive the Bus!' AND author = 'Mo Willems' AND grade_level = 'Kindergarten';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/61JnjSExBVL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'I Love My New Toy!' AND author = 'Mo Willems' AND grade_level = 'Kindergarten';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/71tQc7LhKBL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Can I Play Too?' AND author = 'Mo Willems' AND grade_level = 'Kindergarten';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781423164821_p0_v6_s1200x630.jpg' 
WHERE title = 'Let\'s Go for a Drive!' AND author = 'Mo Willems' AND grade_level = 'Kindergarten';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781423174912_p0_v4_s1200x630.jpg' 
WHERE title = 'A Big Guy Took My Ball!' AND author = 'Mo Willems' AND grade_level = 'Kindergarten';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781423183051_p0_v3_s1200x630.jpg' 
WHERE title = 'I\'m a Frog!' AND author = 'Mo Willems' AND grade_level = 'Kindergarten';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/71YCnIn7ipL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'My Friend Is Sad' AND author = 'Mo Willems' AND grade_level = 'Kindergarten';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780394800165_p0_v10_s1200x630.jpg' 
WHERE title = 'Green Eggs and Ham' AND author = 'Dr. Seuss' AND grade_level = 'Kindergarten';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780394800165_p0_v10_s1200x630.jpg' 
WHERE title = 'Green Eggs and Ham' AND author = 'Dr. Seuss' AND grade_level = '1st Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/81aeV2igJsL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Biscuit Goes to School' AND author = 'Alyssa Satin Capucilli' AND grade_level = '1st Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780064442121_p0_v6_s1200x630.jpg' 
WHERE title = 'Biscuit' AND author = 'Alyssa Satin Capucilli' AND grade_level = '1st Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/61gYTpPyCDL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Biscuit Finds a Friend' AND author = 'Alyssa Satin Capucilli' AND grade_level = '1st Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/71tQc7LhKBL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Can I Play Too?' AND author = 'Mo Willems' AND grade_level = '1st Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781423164821_p0_v6_s1200x630.jpg' 
WHERE title = 'Let\'s Go for a Drive!' AND author = 'Mo Willems' AND grade_level = '1st Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781423174912_p0_v4_s1200x630.jpg' 
WHERE title = 'A Big Guy Took My Ball!' AND author = 'Mo Willems' AND grade_level = '1st Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781423183051_p0_v3_s1200x630.jpg' 
WHERE title = 'I\'m a Frog!' AND author = 'Mo Willems' AND grade_level = '1st Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/7157CblHHcL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Don\'t Let The Pigeon Drive the Bus!' AND author = 'Mo Willems' AND grade_level = '1st Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/71NCN0Aee-L._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Waiting Is Not Easy!' AND author = 'Mo Willems' AND grade_level = '1st Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/71NCN0Aee-L._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Should I Share My Ice Cream?' AND author = 'Mo Willems' AND grade_level = '1st Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781484722626_p0_v2_s1200x630.jpg' 
WHERE title = 'I Really Like Slop!' AND author = 'Mo Willems' AND grade_level = '1st Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781423106869_p0_v5_s1200x630.jpg' 
WHERE title = 'There Is a Bird on Your Head!' AND author = 'Mo Willems' AND grade_level = '1st Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781423179580_p0_v3_s1200x630.jpg' 
WHERE title = 'My New Friend Is So Fun!' AND author = 'Mo Willems' AND grade_level = '1st Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781423133087_p0_v4_s1200x630.jpg' 
WHERE title = 'We Are in a Book!' AND author = 'Mo Willems' AND grade_level = '1st Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/913RtjJj8lL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Pete the Cat: Pete\'s Big Lunch' AND author = 'James Dean' AND grade_level = '1st Grade';
UPDATE books SET cover_url = 'https://i.harperapps.com/covers/9780062110732.jpg' 
WHERE title = 'Pete the Cat: Pete at the Beach' AND author = 'James Dean' AND grade_level = '1st Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/81m-tDWOQTL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Pete the Cat: Too Cool for School' AND author = 'Kimberly Dean' AND grade_level = '1st Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/71DYPJVp-2L._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Pete the Cat: I Love My White Shoes' AND author = 'Eric Litwin' AND grade_level = '1st Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/81pZgIddQQL._UF1000,1000_QL80_.jpg' 
WHERE title = 'Hi! Fly Guy' AND author = 'Tedd Arnold' AND grade_level = '1st Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/81pZgIddQQL._UF1000,1000_QL80_.jpg' 
WHERE title = 'Hi! Fly Guy' AND author = 'Tedd Arnold' AND grade_level = '2nd Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/81m-tDWOQTL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Pete the Cat: Too Cool for School' AND author = 'Kimberly Dean' AND grade_level = '2nd Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/71DYPJVp-2L._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Pete the Cat: I Love My White Shoes' AND author = 'Eric Litwin' AND grade_level = '2nd Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780394800165_p0_v10_s1200x630.jpg' 
WHERE title = 'Green Eggs and Ham' AND author = 'Dr. Seuss' AND grade_level = '2nd Grade';
UPDATE books SET cover_url = 'https://cdn11.bigcommerce.com/s-0f1b1/images/stencil/1280x1280/products/7544/47334/The_Cat_in_the_Hat_Hardcover_Front__53170.1559914007.jpg?c=2?imbypass=on' 
WHERE title = 'The Cat in the Hat' AND author = 'Dr. Seuss' AND grade_level = '2nd Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/7157CblHHcL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Don\'t Let The Pigeon Drive the Bus!' AND author = 'Mo Willems' AND grade_level = '2nd Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/813csV5cPqL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'If You Give a Mouse a Cookie' AND author = 'Laura Numeroff' AND grade_level = '2nd Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780060266868_p0_v3_s1200x630.jpg' 
WHERE title = 'If You Give a Pig a Pancake' AND author = 'Laura Numeroff' AND grade_level = '2nd Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780060283285_p0_v2_s1200x630.jpg' 
WHERE title = 'If You Take a Mouse to School' AND author = 'Laura Numeroff' AND grade_level = '2nd Grade';
UPDATE books SET cover_url = 'https://upload.wikimedia.org/wikipedia/en/b/b5/HungryCaterpillar.JPG' 
WHERE title = 'The Very Hungry Caterpillar' AND author = 'Eric Carle' AND grade_level = '2nd Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/81BzYosm8UL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'The Bad Seed' AND author = 'Jory John' AND grade_level = '2nd Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780062866004_p0_v5_s1200x630.jpg' 
WHERE title = 'The Good Egg' AND author = 'Jory John' AND grade_level = '2nd Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/81kcsNeqOlL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'The Cool Bean' AND author = 'Jory John' AND grade_level = '2nd Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/81yO012wTjL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Click, Clack, Moo: Cows That Type' AND author = 'Doreen Cronin' AND grade_level = '2nd Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780545682923_p0_v1_s600x595.jpg' 
WHERE title = 'There Was an Old Lady Who Swallowed a Bat!' AND author = 'Lucille Colandro' AND grade_level = '2nd Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/81jUSNAg4gL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'There Was a Cold Lady Who Swallowed Some Snow!' AND author = 'Lucille Colandro' AND grade_level = '2nd Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781442402973_p0_v5_s1200x630.jpg' 
WHERE title = 'Creepy Carrots!' AND author = 'Aaron Reynolds' AND grade_level = '2nd Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/81xlkSkquTL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Big Red Lollipop' AND author = 'Rukhsana Khan' AND grade_level = '2nd Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781338741032_p0_v3_s600x595.jpg' 
WHERE title = 'Dog Man' AND author = 'Dav Pilkey' AND grade_level = '2nd Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780062192264_p0_v5_s1200x630.jpg' 
WHERE title = 'Clark the Shark' AND author = 'Bruce Hale' AND grade_level = '2nd Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781338741032_p0_v3_s600x595.jpg' 
WHERE title = 'Dog Man' AND author = 'Dav Pilkey' AND grade_level = '3rd Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781338741049_p0_v3_s1200x630.jpg' 
WHERE title = 'Dog Man Unleashed' AND author = 'Dav Pilkey' AND grade_level = '3rd Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781338741087_p0_v3_s600x595.jpg' 
WHERE title = 'Dog Man: Brawl of the Wild' AND author = 'Dav Pilkey' AND grade_level = '3rd Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781338741070_p0_v3_s1200x630.jpg' 
WHERE title = 'Dog Man: Lord of the Fleas' AND author = 'Dav Pilkey' AND grade_level = '3rd Grade';
UPDATE books SET cover_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRTdashEseEqf9_ukP8tqjjqNzdCMUHyQfznQ&s' 
WHERE title = 'Dog Man: Fetch-22' AND author = 'Dav Pilkey' AND grade_level = '3rd Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/71PmPT6C93L._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Dog Man: Mothering Heights' AND author = 'Dav Pilkey' AND grade_level = '3rd Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781338535624_p0_v6_s1200x630.jpg' 
WHERE title = 'Dog Man: Grime and Punishment' AND author = 'Dav Pilkey' AND grade_level = '3rd Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781338741063_p0_v3_s1200x630.jpg' 
WHERE title = 'Dog Man and Cat Kid' AND author = 'Dav Pilkey' AND grade_level = '3rd Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/91AwBE2IexL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Dog Man: A Tale of Two Kitties' AND author = 'Dav Pilkey' AND grade_level = '3rd Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781338801910_p0_v7_s1200x630.jpg' 
WHERE title = 'Dog Man: Twenty Thousand Fleas Under the Sea' AND author = 'Dav Pilkey' AND grade_level = '3rd Grade';
UPDATE books SET cover_url = 'https://online.fliphtml5.com/jozwk/fsgh/files/large/c74d97b01eae257e44aa9d5bade97baf.webp?1660917837' 
WHERE title = 'Charlotte\'s Web' AND author = 'E.B. White' AND grade_level = '3rd Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781536214352_p0_v2_s600x595.jpg' 
WHERE title = 'Because of Winn-Dixie' AND author = 'Kate DiCamillo' AND grade_level = '3rd Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/71jKDOvOwqL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Scaredy Squirrel' AND author = 'Mélanie Watt' AND grade_level = '3rd Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/910+U8mCK4L._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'The True Story of the 3 Little Pigs' AND author = 'Jon Scieszka' AND grade_level = '3rd Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780439598385_p0_v4_s1200x630.jpg' 
WHERE title = 'A Bad Case of Stripes' AND author = 'David Shannon' AND grade_level = '3rd Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781947277311_p0_v8_s1200x630.jpg' 
WHERE title = 'I Need My Monster' AND author = 'Amanda Noll' AND grade_level = '3rd Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780394800165_p0_v10_s1200x630.jpg' 
WHERE title = 'Green Eggs and Ham' AND author = 'Dr. Seuss' AND grade_level = '3rd Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/815sKoUHKLL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'The One and Only Ivan' AND author = 'Katherine Applegate' AND grade_level = '3rd Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780063444010_p0_v1_s1200x630.jpg' 
WHERE title = 'The Smart Cookie' AND author = 'Jory John' AND grade_level = '3rd Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/813csV5cPqL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'If You Give a Mouse a Cookie' AND author = 'Laura Numeroff' AND grade_level = '3rd Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780142408810_p0_v4_s1200x630.jpg' 
WHERE title = 'Tales of a Fourth Grade Nothing' AND author = 'Judy Blume' AND grade_level = '4th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/813csV5cPqL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Because of Winn-Dixie' AND author = 'Kate DiCamillo' AND grade_level = '4th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419766947_p1_v4_s600x595.jpg' 
WHERE title = 'Diary of a Wimpy Kid: No Brainer' AND author = 'Jeff Kinney' AND grade_level = '4th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741852_p0_v1_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid' AND author = 'Jeff Kinney' AND grade_level = '4th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741982_p0_v2_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: The Getaway' AND author = 'Jeff Kinney' AND grade_level = '4th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741869_p0_v1_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: Rodrick Rules' AND author = 'Jeff Kinney' AND grade_level = '4th Grade';
UPDATE books SET cover_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRJCMNzW-39WnfujRZzcuEhLYuVDp_c1WpSTQ&s' 
WHERE title = 'Diary of a Wimpy Kid: Dog Days' AND author = 'Jeff Kinney' AND grade_level = '4th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741876_p0_v1_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: The Last Straw' AND author = 'Jeff Kinney' AND grade_level = '4th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741944_p0_v1_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: Hard Luck' AND author = 'Jeff Kinney' AND grade_level = '4th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741890_p0_v1_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: The Ugly Truth' AND author = 'Jeff Kinney' AND grade_level = '4th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741951_p0_v1_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: The Long Haul' AND author = 'Jeff Kinney' AND grade_level = '4th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741937_p0_v1_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: The Third Wheel' AND author = 'Jeff Kinney' AND grade_level = '4th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419748684_p0_v2_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: The Deep End' AND author = 'Jeff Kinney' AND grade_level = '4th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741999_p0_v2_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: The Meltdown' AND author = 'Jeff Kinney' AND grade_level = '4th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741968_p0_v1_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: Old School' AND author = 'Jeff Kinney' AND grade_level = '4th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/81hF6AzGs1L._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Diary of a Wimpy Kid: Cabin Fever' AND author = 'Jeff Kinney' AND grade_level = '4th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419749155_p0_v4_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: Big Shot' AND author = 'Jeff Kinney' AND grade_level = '4th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419739033_p0_v5_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: Wrecking Ball' AND author = 'Jeff Kinney' AND grade_level = '4th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741975_p0_v1_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: Double Down' AND author = 'Jeff Kinney' AND grade_level = '4th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/819bxLMj91L._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Diary of a Wimpy Kid: Diper Överlöde' AND author = 'Jeff Kinney' AND grade_level = '4th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780375869020_p0_v9_s1200x630.jpg' 
WHERE title = 'Wonder' AND author = 'R.J. Palacio' AND grade_level = '5th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781416936473_p0_v3_s1200x630.jpg' 
WHERE title = 'Hatchet' AND author = 'Gary Paulsen' AND grade_level = '5th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/91rgSkIk1kL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Number the Stars' AND author = 'Lois Lowry' AND grade_level = '5th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/81ZPONpE+qL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Esperanza Rising' AND author = 'Pam Muñoz Ryan' AND grade_level = '5th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/71pziPx5qpL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Holes' AND author = 'Louis Sachar' AND grade_level = '5th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419766947_p1_v4_s600x595.jpg' 
WHERE title = 'Diary of a Wimpy Kid: No Brainer' AND author = 'Jeff Kinney' AND grade_level = '5th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741852_p0_v1_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid' AND author = 'Jeff Kinney' AND grade_level = '5th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741982_p0_v2_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: The Getaway' AND author = 'Jeff Kinney' AND grade_level = '5th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741869_p0_v1_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: Rodrick Rules' AND author = 'Jeff Kinney' AND grade_level = '5th Grade';
UPDATE books SET cover_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRJCMNzW-39WnfujRZzcuEhLYuVDp_c1WpSTQ&s' 
WHERE title = 'Diary of a Wimpy Kid: Dog Days' AND author = 'Jeff Kinney' AND grade_level = '5th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741876_p0_v1_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: The Last Straw' AND author = 'Jeff Kinney' AND grade_level = '5th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741944_p0_v1_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: Hard Luck' AND author = 'Jeff Kinney' AND grade_level = '5th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741890_p0_v1_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: The Ugly Truth' AND author = 'Jeff Kinney' AND grade_level = '5th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741951_p0_v1_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: The Long Haul' AND author = 'Jeff Kinney' AND grade_level = '5th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741937_p0_v1_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: The Third Wheel' AND author = 'Jeff Kinney' AND grade_level = '5th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419748684_p0_v2_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: The Deep End' AND author = 'Jeff Kinney' AND grade_level = '5th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741999_p0_v2_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: The Meltdown' AND author = 'Jeff Kinney' AND grade_level = '5th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/81hF6AzGs1L._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Diary of a Wimpy Kid: Cabin Fever' AND author = 'Jeff Kinney' AND grade_level = '5th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419749155_p0_v4_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: Big Shot' AND author = 'Jeff Kinney' AND grade_level = '5th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/819bxLMj91L._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Diary of a Wimpy Kid: Diper Överlöde' AND author = 'Jeff Kinney' AND grade_level = '5th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781416936473_p0_v3_s1200x630.jpg' 
WHERE title = 'Hatchet' AND author = 'Gary Paulsen' AND grade_level = '6th Grade';
UPDATE books SET cover_url = 'https://books.disney.com/content/uploads/2013/09/9780786856299.jpg' 
WHERE title = 'The Lightning Thief' AND author = 'Rick Riordan' AND grade_level = '6th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/91rgSkIk1kL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Number the Stars' AND author = 'Lois Lowry' AND grade_level = '6th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/81t0+y7sfiL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Bud, Not Buddy' AND author = 'Christopher Paul Curtis' AND grade_level = '6th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780375869020_p0_v9_s1200x630.jpg' 
WHERE title = 'Wonder' AND author = 'R.J. Palacio' AND grade_level = '6th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/71un2hI4mcL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'The Hunger Games' AND author = 'Suzanne Collins' AND grade_level = '6th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/91R7BN6VolL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Freak the Mighty' AND author = 'Rodman Philbrick' AND grade_level = '6th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419766947_p1_v4_s600x595.jpg' 
WHERE title = 'Diary of a Wimpy Kid: No Brainer' AND author = 'Jeff Kinney' AND grade_level = '6th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741852_p0_v1_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid' AND author = 'Jeff Kinney' AND grade_level = '6th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741982_p0_v2_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: The Getaway' AND author = 'Jeff Kinney' AND grade_level = '6th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741869_p0_v1_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: Rodrick Rules' AND author = 'Jeff Kinney' AND grade_level = '6th Grade';
UPDATE books SET cover_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRJCMNzW-39WnfujRZzcuEhLYuVDp_c1WpSTQ&s' 
WHERE title = 'Diary of a Wimpy Kid: Dog Days' AND author = 'Jeff Kinney' AND grade_level = '6th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741876_p0_v1_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: The Last Straw' AND author = 'Jeff Kinney' AND grade_level = '6th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741944_p0_v1_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: Hard Luck' AND author = 'Jeff Kinney' AND grade_level = '6th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741890_p0_v1_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: The Ugly Truth' AND author = 'Jeff Kinney' AND grade_level = '6th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741951_p0_v1_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: The Long Haul' AND author = 'Jeff Kinney' AND grade_level = '6th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741937_p0_v1_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: The Third Wheel' AND author = 'Jeff Kinney' AND grade_level = '6th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741999_p0_v2_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: The Meltdown' AND author = 'Jeff Kinney' AND grade_level = '6th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419749155_p0_v4_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: Big Shot' AND author = 'Jeff Kinney' AND grade_level = '6th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/819bxLMj91L._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Diary of a Wimpy Kid: Diper Överlöde' AND author = 'Jeff Kinney' AND grade_level = '6th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781416936473_p0_v3_s1200x630.jpg' 
WHERE title = 'Hatchet' AND author = 'Gary Paulsen' AND grade_level = '7th Grade';
UPDATE books SET cover_url = 'https://books.disney.com/content/uploads/2013/09/9780786856299.jpg' 
WHERE title = 'The Lightning Thief' AND author = 'Rick Riordan' AND grade_level = '7th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/71un2hI4mcL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'The Hunger Games' AND author = 'Suzanne Collins' AND grade_level = '7th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/61IvEGeD5bL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'The Outsiders' AND author = 'S.E. Hinton' AND grade_level = '7th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780544336261_p0_v7_s600x595.jpg' 
WHERE title = 'The Giver' AND author = 'Lois Lowry' AND grade_level = '7th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780547577319_p0_v2_s1200x630.jpg' 
WHERE title = 'A Long Walk to Water: Based on a True Story' AND author = 'Linda Sue Park' AND grade_level = '7th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/91ELsklZazL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Refugee' AND author = 'Alan Gratz' AND grade_level = '7th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/91R7BN6VolL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Freak the Mighty' AND author = 'Rodman Philbrick' AND grade_level = '7th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781416968290_p0_v17_s600x595.jpg' 
WHERE title = 'The Summer I Turned Pretty' AND author = 'Jenny Han' AND grade_level = '7th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780545586177_p0_v2_s600x595.jpg' 
WHERE title = 'Catching Fire' AND author = 'Suzanne Collins' AND grade_level = '7th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419766947_p1_v4_s600x595.jpg' 
WHERE title = 'Diary of a Wimpy Kid: No Brainer' AND author = 'Jeff Kinney' AND grade_level = '7th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741852_p0_v1_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid' AND author = 'Jeff Kinney' AND grade_level = '7th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741982_p0_v2_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: The Getaway' AND author = 'Jeff Kinney' AND grade_level = '7th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741869_p0_v1_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: Rodrick Rules' AND author = 'Jeff Kinney' AND grade_level = '7th Grade';
UPDATE books SET cover_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRJCMNzW-39WnfujRZzcuEhLYuVDp_c1WpSTQ&s' 
WHERE title = 'Diary of a Wimpy Kid: Dog Days' AND author = 'Jeff Kinney' AND grade_level = '7th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741937_p0_v1_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: The Third Wheel' AND author = 'Jeff Kinney' AND grade_level = '7th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741999_p0_v2_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: The Meltdown' AND author = 'Jeff Kinney' AND grade_level = '7th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419749155_p0_v4_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid: Big Shot' AND author = 'Jeff Kinney' AND grade_level = '7th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/819bxLMj91L._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Diary of a Wimpy Kid: Diper Överlöde' AND author = 'Jeff Kinney' AND grade_level = '7th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780439064866_p0_v3_s600x595.jpg' 
WHERE title = 'Harry Potter and the Chamber of Secrets' AND author = 'J.K. Rowling' AND grade_level = '7th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/71un2hI4mcL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'The Hunger Games' AND author = 'Suzanne Collins' AND grade_level = '8th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/61IvEGeD5bL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'The Outsiders' AND author = 'S.E. Hinton' AND grade_level = '8th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780544336261_p0_v7_s600x595.jpg' 
WHERE title = 'The Giver' AND author = 'Lois Lowry' AND grade_level = '8th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781416936473_p0_v3_s1200x630.jpg' 
WHERE title = 'Hatchet' AND author = 'Gary Paulsen' AND grade_level = '8th Grade';
UPDATE books SET cover_url = 'https://books.disney.com/content/uploads/2013/09/9780786856299.jpg' 
WHERE title = 'The Lightning Thief' AND author = 'Rick Riordan' AND grade_level = '8th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781416968290_p0_v17_s600x595.jpg' 
WHERE title = 'The Summer I Turned Pretty' AND author = 'Jenny Han' AND grade_level = '8th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780545586177_p0_v2_s600x595.jpg' 
WHERE title = 'Catching Fire' AND author = 'Suzanne Collins' AND grade_level = '8th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780439064866_p0_v3_s600x595.jpg' 
WHERE title = 'Harry Potter and the Chamber of Secrets' AND author = 'J.K. Rowling' AND grade_level = '8th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/81Z3v51bC5L._UF1000,1000_QL80_.jpg' 
WHERE title = 'The Tell-Tale Heart' AND author = 'Edgar Allen Poe' AND grade_level = '8th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/91ELsklZazL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Refugee' AND author = 'Alan Gratz' AND grade_level = '8th Grade';
UPDATE books SET cover_url = 'https://cdn.kobo.com/book-images/6b90aeaa-8428-4520-8b24-eb8012fc0da6/1200/1200/False/the-monkey-s-paw-16.jpg' 
WHERE title = 'The Monkey\'s Paw' AND author = 'W.W. Jacobs' AND grade_level = '8th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/51Eyjz65gyL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'The Diary of Anne Frank' AND author = 'Frances Goodrich' AND grade_level = '8th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/91aSuSAA1qL._UF1000,1000_QL80_.jpg' 
WHERE title = 'The Boy in the Striped Pajamas' AND author = 'John Boyne' AND grade_level = '8th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/91NBA4uHVKL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Night' AND author = 'Elie Wiesel' AND grade_level = '8th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/81OhJpf3fYL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'It\'s Not Summer Without You' AND author = 'Jenny Han' AND grade_level = '8th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/91-fE4Scx8L._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'The Lost Hero' AND author = 'Rick Riordan' AND grade_level = '8th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/81O7u0dGaWL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'To Kill a Mockingbird' AND author = 'Harper Lee' AND grade_level = '8th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419766947_p1_v4_s600x595.jpg' 
WHERE title = 'Diary of a Wimpy Kid: No Brainer' AND author = 'Jeff Kinney' AND grade_level = '8th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781419741852_p0_v1_s1200x630.jpg' 
WHERE title = 'Diary of a Wimpy Kid' AND author = 'Jeff Kinney' AND grade_level = '8th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/819bxLMj91L._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Diary of a Wimpy Kid: Diper Överlöde' AND author = 'jeff Kinney' AND grade_level = '8th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/81O7u0dGaWL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'To Kill a Mockingbird' AND author = 'Harper Lee' AND grade_level = '9th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780439064866_p0_v3_s600x595.jpg' 
WHERE title = 'Harry Potter and the Chamber of Secrets' AND author = 'J.K. Rowling' AND grade_level = '9th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/71un2hI4mcL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'The Hunger Games' AND author = 'Suzanne Collins' AND grade_level = '9th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/61IvEGeD5bL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'The Outsiders' AND author = 'S.E. Hinton' AND grade_level = '9th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781416936473_p0_v3_s1200x630.jpg' 
WHERE title = 'Hatchet' AND author = 'Gary Paulsen' AND grade_level = '9th Grade';
UPDATE books SET cover_url = 'https://books.disney.com/content/uploads/2013/09/9780786856299.jpg' 
WHERE title = 'The Lightning Thief' AND author = 'Rick Riordan' AND grade_level = '9th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781416968290_p0_v17_s600x595.jpg' 
WHERE title = 'The Summer I Turned Pretty' AND author = 'Jenny Han' AND grade_level = '9th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780545586177_p0_v2_s600x595.jpg' 
WHERE title = 'Catching Fire' AND author = 'Suzanne Collins' AND grade_level = '9th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/91ELsklZazL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Refugee' AND author = 'Alan Gratz' AND grade_level = '9th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/91NBA4uHVKL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Night' AND author = 'Elie Wiesel' AND grade_level = '9th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/91-fE4Scx8L._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'The Lost Hero' AND author = 'Rick Riordan' AND grade_level = '9th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/71+tuHzXknL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'We Were Liars' AND author = 'E. Lockhart' AND grade_level = '9th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781451621709_p0_v6_s1200x630.jpg' 
WHERE title = 'Romeo and Juliet' AND author = 'William Shakespeare' AND grade_level = '9th Grade';
UPDATE books SET cover_url = 'https://images.penguinrandomhouse.com/cover/9780142000670' 
WHERE title = 'Of Mice and Men' AND author = 'John Steinbeck' AND grade_level = '9th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781627300667_p0_v1_s600x595.jpg' 
WHERE title = 'The Most Dangerous Game' AND author = 'Richard Connell' AND grade_level = '9th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/51oIaUDi2wL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Animal Farm' AND author = 'George Orwell' AND grade_level = '9th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/61sKsbPb5GL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Fahrenheit 451 (English)' AND author = 'Ray Bradbury' AND grade_level = '9th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780399501487_p0_v5_s1200x630.jpg' 
WHERE title = 'Lord of the Flies' AND author = 'William Golding' AND grade_level = '9th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781501110368_p0_v16_s600x595.jpg' 
WHERE title = 'It Ends with Us' AND author = 'Colleen Hoover' AND grade_level = '9th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/71vgZlr-ZTL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Oracle: River of Ore' AND author = 'C.W. Trisef' AND grade_level = '9th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/51oIaUDi2wL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Animal Farm' AND author = 'George Orwell' AND grade_level = '10th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/61sKsbPb5GL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Fahrenheit 451 (English)' AND author = 'Ray Bradbury' AND grade_level = '10th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780399501487_p0_v5_s1200x630.jpg' 
WHERE title = 'Lord of the Flies' AND author = 'William Golding' AND grade_level = '10th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781501110368_p0_v16_s600x595.jpg' 
WHERE title = 'It Ends with Us' AND author = 'Colleen Hoover' AND grade_level = '10th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/71vgZlr-ZTL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Oracle: River of Ore' AND author = 'C.W. Trisef' AND grade_level = '10th Grade';
UPDATE books SET cover_url = 'https://images.penguinrandomhouse.com/cover/9780142000670' 
WHERE title = 'Of Mice and Men' AND author = 'John Steinbeck' AND grade_level = '10th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/81O7u0dGaWL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'To Kill a Mockingbird' AND author = 'Harper Lee' AND grade_level = '10th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780545586177_p0_v2_s600x595.jpg' 
WHERE title = 'Catching Fire' AND author = 'Suzanne Collins' AND grade_level = '10th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/91ELsklZazL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Refugee' AND author = 'Alan Gratz' AND grade_level = '10th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/81uRYzv9UsL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Julius Caesar' AND author = 'William Shakespeare' AND grade_level = '10th Grade';
UPDATE books SET cover_url = 'https://d28hgpri8am2if.cloudfront.net/book_images/onix/cvr9781451694727/macbeth-9781451694727_hr.jpg' 
WHERE title = 'Macbeth' AND author = 'William Shakespeare' AND grade_level = '10th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/A1GErcFPllL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Hideout' AND author = 'Watt Key' AND grade_level = '10th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/71evArAk4wL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'All American Boys' AND author = 'Jason Reynolds' AND grade_level = '10th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781476753188_p0_v11_s1200x630.jpg' 
WHERE title = 'Ugly Love' AND author = 'Colleen Hoover' AND grade_level = '10th Grade';
UPDATE books SET cover_url = 'https://d28hgpri8am2if.cloudfront.net/book_images/cvr9781416599685_9781416599685_hr.jpg' 
WHERE title = 'The Metamorphosis' AND author = 'Franz Kafka' AND grade_level = '10th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780385474542_p0_v6_s600x595.jpg' 
WHERE title = 'Things Fall Apart' AND author = 'Chinua Achebe' AND grade_level = '10th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/71un2hI4mcL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'The Hunger Games' AND author = 'Suzanne Collins' AND grade_level = '10th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781416936473_p0_v3_s1200x630.jpg' 
WHERE title = 'Hatchet' AND author = 'Gary Paulsen' AND grade_level = '10th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/71+tuHzXknL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'We Were Liars' AND author = 'E. Lockhart' AND grade_level = '10th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/91NBA4uHVKL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Night' AND author = 'Elie Wiesel' AND grade_level = '10th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781501110368_p0_v16_s600x595.jpg' 
WHERE title = 'It Ends with Us' AND author = 'Colleen Hoover' AND grade_level = '11th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781668001226_p0_v10_s600x595.jpg' 
WHERE title = 'It Starts with Us' AND author = 'Colleen Hoover' AND grade_level = '11th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/71vgZlr-ZTL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Oracle: River of Ore' AND author = 'C.W. Trisef' AND grade_level = '11th Grade';
UPDATE books SET cover_url = 'https://images.penguinrandomhouse.com/cover/9780142000670' 
WHERE title = 'Of Mice and Men' AND author = 'John Steinbeck' AND grade_level = '11th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/81O7u0dGaWL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'To Kill a Mockingbird' AND author = 'Harper Lee' AND grade_level = '11th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780545586177_p0_v2_s600x595.jpg' 
WHERE title = 'Catching Fire' AND author = 'Suzanne Collins' AND grade_level = '11th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/91ELsklZazL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Refugee' AND author = 'Alan Gratz' AND grade_level = '11th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/61sKsbPb5GL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Fahrenheit 451 (English)' AND author = 'Ray Bradbury' AND grade_level = '11th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/71un2hI4mcL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'The Hunger Games' AND author = 'Suzanne Collins' AND grade_level = '11th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/71+tuHzXknL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'We Were Liars' AND author = 'E. Lockhart' AND grade_level = '11th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781476753188_p0_v11_s1200x630.jpg' 
WHERE title = 'Ugly Love' AND author = 'Colleen Hoover' AND grade_level = '11th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/91-fE4Scx8L._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'The Lost Hero' AND author = 'Rick Riordan' AND grade_level = '11th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/81TLiZrasVL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'The Great Gatsby' AND author = 'F. Scott Fitzgerald' AND grade_level = '11th Grade';
UPDATE books SET cover_url = 'https://images.penguinrandomhouse.com/cover/9780142437339' 
WHERE title = 'The Crucible' AND author = 'Arthur Miller' AND grade_level = '11th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/91XrObgq4GL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Born a Crime: Stories from a South African Childhood' AND author = 'Trevor Noah' AND grade_level = '11th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/71YvIyTP6fL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Their Eyes Were Watching God' AND author = 'Zora Neale Hurston' AND grade_level = '11th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/A1GErcFPllL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Hideout' AND author = 'Watt Key' AND grade_level = '11th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780439064866_p0_v3_s600x595.jpg' 
WHERE title = 'Harry Potter and the Chamber of Secrets' AND author = 'J.K. Rowling' AND grade_level = '11th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780452264014_p0_v2_s1200x630.jpg' 
WHERE title = 'Fences' AND author = 'August Wilson' AND grade_level = '11th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781416936473_p0_v3_s1200x630.jpg' 
WHERE title = 'Hatchet' AND author = 'Gary Paulsen' AND grade_level = '11th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/91ELsklZazL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Refugee' AND author = 'Alan Gratz' AND grade_level = '12th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/61sKsbPb5GL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Fahrenheit 451 (English)' AND author = 'Ray Bradbury' AND grade_level = '12th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/71un2hI4mcL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'The Hunger Games' AND author = 'Suzanne Collins' AND grade_level = '12th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/71+tuHzXknL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'We Were Liars' AND author = 'E. Lockhart' AND grade_level = '12th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781476753188_p0_v11_s1200x630.jpg' 
WHERE title = 'Ugly Love' AND author = 'Colleen Hoover' AND grade_level = '12th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/91-fE4Scx8L._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'The Lost Hero' AND author = 'Rick Riordan' AND grade_level = '12th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/81TLiZrasVL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'The Great Gatsby' AND author = 'F. Scott Fitzgerald' AND grade_level = '12th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781416936473_p0_v3_s1200x630.jpg' 
WHERE title = 'Hatchet' AND author = 'Gary Paulsen' AND grade_level = '12th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/A1GErcFPllL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Hideout' AND author = 'Watt Key' AND grade_level = '12th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780439064866_p0_v3_s600x595.jpg' 
WHERE title = 'Harry Potter and the Chamber of Secrets' AND author = 'J.K. Rowling' AND grade_level = '12th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781501110368_p0_v16_s600x595.jpg' 
WHERE title = 'It Ends with Us' AND author = 'Colleen Hoover' AND grade_level = '12th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9781435159624_p0_v8_s600x595.jpg' 
WHERE title = 'Frankenstein (Unabridged)' AND author = 'Mary Shelley' AND grade_level = '12th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/71vgZlr-ZTL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Oracle: River of Ore' AND author = 'C.W. Trisef' AND grade_level = '12th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780743477123_p0_v5_s1200x630.jpg' 
WHERE title = 'Hamlet' AND author = 'William Shakespeare' AND grade_level = '12th Grade';
UPDATE books SET cover_url = 'https://d28hgpri8am2if.cloudfront.net/book_images/onix/cvr9781451694727/macbeth-9781451694727_hr.jpg' 
WHERE title = 'Macbeth' AND author = 'William Shakespeare' AND grade_level = '12th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/51oIaUDi2wL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Animal Farm' AND author = 'George Orwell' AND grade_level = '12th Grade';
UPDATE books SET cover_url = 'https://m.media-amazon.com/images/I/71+Fv87ZoqL._AC_UF1000,1000_QL80_.jpg' 
WHERE title = 'Sing, Unburied, Sing' AND author = 'Jesmyn Ward' AND grade_level = '12th Grade';
UPDATE books SET cover_url = 'https://images.penguinrandomhouse.com/cover/9780142000670' 
WHERE title = 'Of Mice and Men' AND author = 'John Steinbeck' AND grade_level = '12th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780399501487_p0_v5_s1200x630.jpg' 
WHERE title = 'Lord of the Flies' AND author = 'William Golding' AND grade_level = '12th Grade';
UPDATE books SET cover_url = 'https://prodimage.images-bn.com/pimages/9780393320978_p0_v2_s1200x630.jpg' 
WHERE title = 'Beowulf' AND author = 'Anonymous' AND grade_level = '12th Grade';

-- Check results
SELECT 
    COUNT(*) as total_books,
    COUNT(cover_url) as books_with_covers,
    ROUND((COUNT(cover_url) / COUNT(*)) * 100, 2) as percentage_with_covers
FROM books;

-- Sample books with covers
SELECT title, author, grade_level, LEFT(cover_url, 50) as cover_preview 
FROM books WHERE cover_url IS NOT NULL LIMIT 10;
