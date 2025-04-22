/* 
Lecture #6 Feb 8
*/

/* Cartesian / Cross Joins */
-- Up to now, we’ve being doing Cartesian joins
-- Also called Cross joins
select *
from instructor i, teaches t
where i.ID = t.ID
order by i.name;

select *
from instructor i cross join teaches t
where i.ID = t.ID
order by i.name;

/* Natural Join in SQL */

-- Natural join matches tuples with the same values for all common
-- attributes, and retains only one copy of each common column.
	-- Takes advantage of the fact that most times we’re equating attributes
	-- in one table to those in a 2nd table.
    
-- List the names of instructors along with the course ID of the courses that they taught
select name, course_id
from students, takes
where student.ID = takes.ID;
-- Same query in SQL with “natural join” construct
select name, course_id
from student natural join takes;

-- The from clause can have multiple relations combined using natural join:
	-- select A1, A2, … An
	-- from r1 natural join r2 natural join .. natural join rn
	-- where P ;
    
select *
from student natural join takes;
-- the ID column occurs only once when the natural join is used.
-- In a cross join, there would be 2 ID columns: one from each table.
	-- Column order in a natural join:
	-- 1) Common columns
	-- 2) Columns unique to the table before join
	-- 3) Columns unique to the table after join
    
/* Beware of unrelated attributes with same name which get equated incorrectly */
-- Example -- List the names of student’s instructors along with the titles of courses that the students have taken
	-- Incorrect version:c 
select name, title
from student natural join takes natural join course;
-- This query omits all (student name, course title) pairs where the student
-- takes a course in a department other than the student's own department.

-- The join was done on dept_name and course_id
-- Problem!!!
-- dept_name in student natural join takes comes from the student table = major
-- dept_name in course means the department giving the class.
-- This query omits all (student name, course title) pairs where the student takes a course
-- in a department other than the student's own department.

-- Correct version
select name, title
from student natural join takes, course
where takes.course_id = course.course_id;
/* This is a natural join combined with a cross join
   The natural join is done before the application of the where clause
   takes.course_id refers to the course_id field of the natural join since it came
from the takes relation
   Can also write this as */
select name, title
from student natural join takes as st, course as c
where st.course_id = c.course_id;

/* 
Practice
Get a list of all instructors, showing each instructor’s name and the number of
sections taught. Omit any instructors who have not taught any section. Order
the list in descending order of the number of sections. Do not use subqueries. */
select name, count(sec_id) as Number_of_sections
from instructor natural join teaches
group by ID
order by Number_of_sections desc;
-- Instructor and teaches only have ID (the instructor’s ID) column in common



/* 
Join with Using Clause 
-- To avoid the danger of equating attributes erroneously, we can use the
-- “using” construct that allows us to specify exactly which columns should be equated.
*/

-- Query example
select name, title
from (student natural join takes) join course using (course_id);



/* 
Join with On Clause  
-- The on condition allows a general predicate over the relations being joined
-- This predicate is written like a where clause predicate except for the use of the keyword on
*/

-- Query example
select *
from student join takes on student.ID = takes.ID;
-- The on condition above specifies that a tuple from student matches a
-- tuple from takes if their ID values are equal.
	-- Equivalent to:
select *
from student , takes
where student.ID = takes.ID;
-- Unlike the natural join, the ID column will appear twice: once
-- for the student table and again for the takes table.


/* 
Outer Join 

§ An extension of the join operation that avoids loss of information.

§ Computes the join and then adds tuples form one relation that does not
match tuples in the other relation to the result of the join.

§ Uses null values.

§ Three forms of outer join:
	• left outer join
	• right outer join
	• full outer join 
*/



/* Left Outer Join */
-- course natural left outer join prereq
-- course natural left outer join prereq using (course_id) -- Note: mySQL does not support this construct
-- course left outer join prereq on (course.course_id = prereq.course_id)

-- full output:
select c.course_id, title, dept_name, credits, prereq_id
from course c left outer join prereq p on (c.course_id = p.course_id);

/* 
Right Outer Join 
-- course natural right outer join prereq
-- course natural right outer join prereq using (course_id) -- Note: mySQL does not support this construct
-- course right outer join prereq on (course.course_id = prereq.course_id)
*/

/* 
Full Outer Join
§ course natural full outer join prereq
§ course natural full outer join prereq using (course_id)
§ course full outer join prereq on (course.course_id = prereq.course_id)
§ course full join prereq on (course.course_id = prereq.course_id)

MySQL does not support full joins
*/

/*
Inner Join
§ course natural inner join prereq
§ course natural inner outer join prereq using (course_id)
§ course inner join prereq on (course.course_id = prereq.course_id)
*/

/*
Joined Types and Conditions

	§ Join operations take two relations and return as a result another
	  relation.
      
	§ These additional operations are typically used as subquery expressions
	  in the from clause

	§ Join condition – defines which tuples in the two relations match.
    
	§ Join type – defines how tuples in each relation that do not match any
	  tuple in the other relation (based on the join condition) are treated.
*/



/* Cross Join vs Inner Join vs “Comma” Join */

-- What’s the difference between
select *
from A, B
where A.id = B.id;

select *
from A cross join B
where A.id = B.id;

select *
from A inner join B on (A.id = B.id);

select *
from A join B on (A.id = B.id);

/* They are equivalently the same!!
All return tuples with no null
values in the join (e.g. in the
where clause or on statement) */ 



/* 
Precedence
	§ There is an order of precedence:
		• cross join, natural join, outer join, inner join will all be done 
          before a comma (Cartesian)
          
		• from A, B join C on (B.b = C.c)
		  B join C on (B.b = C.c) will be done first 
          The result of that join will then be joined with A
*/ 



/* Practice
	Get a list of all instructors, showing each instructor’s name and the number of
	sections taught. Make sure to show the number of sections as 0 for
	instructors who have not taught any section. Do not use subqueries.
*/
select name, count(sec_id) as Number_of_sections
from instructor natural left outer join teaches
group by name;
/* Note that this query can not be written using count(*) since that would also
count nulls. You can put any attribute from teaches that does not appear in
instructor into the count() */



/* Practice
	Display the list of all departments, with the total number of instructors in each
	department, without using subqueries. Make sure to show departments that
	have no instructors, and list those departments with an instructor count of zero
*/
select dept_name, count(ID) as number_of_instructors
from department natural left outer join instructor
group by dept_name;





