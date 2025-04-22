/* 
Lecture #5 Tuesday Feb 6


SQL provides a mechanism for the nesting of subqueries.
	• A subquery is a select-from-where expression that is nested within another query.

The nesting can be done in the following SQL query
	select A_1, A_2, ..., A_n
	from r_1, r_2, ..., r_m
	where P
    
as follows:
	• From clause: ri can be replaced by any valid subquery
	• Where clause: P can be replaced with an expression of the form:
		B <operation> (subquery)
	B is an attribute and <operation> to be defined later.
	• Select clause:
	A_i can be replaced be a subquery that generates a single value.
*/


-- Find courses offered in Fall 2017 and in Spring 2018
-- Previously done with an intersect (courses taught in both semesters)

(select course_id from section where semester = 'Fall' and year = 2017);
intersect
(select course_id from section where semester = 'Spring' and year = 2018);

-- With a nested query and using “in”
select distinct course_id
from section
where semester = 'Fall' and year= 2017 and
	course_id in (select course_id
		from section
		where semester = 'Spring' and year= 2018);




/* Practice: Set Membership */ 

-- Using nested subqueries and ”in”, select the dept_name from department that is located in Painter and has a budget > 100000
select dept_name
from department
where building = 'Painter' and 
	dept_name in (select dept_name
					from department 
					where budget > 100000);

-- Find all instructors earning the highest salary (there may be more than one with the same salary)
select name
from instructor
where salary = (select max(salary) 
					from instructor);



/* Set Comparison – “some” Clause */ 

-- Find names of instructors with salary greater than that of some (at least one) instructor in the Biology dept
select distinct T.name
from instructor as T, instructor as S
where T.salary > S.salary and S.dept_name = 'Biology';

-- Same query using > some clause
select name
from instructor
where salary > some (select salary
						from instructor
						where dept_name = 'Biology');



/* Set Comparison – “all” Clause */ 

-- Find the names of all instructors whose salary is greater than the salary of all instructors in the Biology department.
select name
from instructor
where salary > all (select salary
						from instructor
						where dept_name = 'Biology');



/* Use of “exists” Clause */ 

-- Yet another way of specifying the query “Find all courses taught in both the
-- Fall 2017 semester and in the Spring 2018 semester” (used intersect previously)
select course_id
from section as S
where semester = 'Fall' and year = 2017 and
	exists (select *
			from section as T
			where semester = 'Spring' and year= 2018
				and S.course_id = T.course_id);

-- Correlation name – variable S in the outer query
-- Correlated subquery – a subquery that uses a correlation name from an outer query



/* Use of “not exists” Clause */ 

-- Find all students who have taken all courses offered in the Biology department.

select distinct S.ID, S.name
from student as S
-- subquery returns nothing (in this case... subquery returns nothing for that specific student)
where not exists ((select course_id
					from course
					where dept_name = 'Biology')
				    except
					(select T.course_id
					from takes as T
					where S.ID = T.ID));
	-- First nested query lists all courses offered in Biology
	-- Second nested query lists all courses a particular student took
	-- Except removes the student’s courses from the overall list
	-- If there are no courses left for that student, then we’ve found one of the students we’re looking for.
-- Note: Cannot write this query using = all and its variants



/* Practice: Set Comparisons */ 

-- Select the student names and the names of the courses they are taking
-- now or have taken in the past, but exclude anyone in the Robotics class.

select s.name, c.title
from student s, takes t, section sec, course c
where s.id = t.id
and t.course_id = sec.course_id
and t.sec_id = sec.sec_id
and t.semester = sec.semester
and t.year = sec.year
and sec.course_id = c.course_id
and not exists 
	(select *
    from course c2
    where c.course_id = c2.course_id
    and c2.title = 'Robotics');




/* Subqueries in the From Clause */

-- SQL allows a subquery expression to be used in the from clause
-- Find the average instructors’ salaries of those departments where the average salary is greater than $42,000.
select dept_name, avg_salary
from ( select dept_name, avg (salary) as avg_salary
		from instructor
		group by dept_name)
where avg_salary > 42000;
-- Note that we do not need to use the having clause

-- Another way to write above query
select dept_name, avg_salary
from ( select dept_name, avg (salary)
		from instructor
		group by dept_name)
			as dept_avg (dept_name, avg_salary)
where avg_salary > 42000;



/* With Clause */ 

-- The with clause provides a way of defining a temporary relation whose
-- definition is available only to the query in which the with clause occurs.

	-- with query_name (list of attributes being returned) as

-- Find all departments with the maximum budget
with max_budget (value) as
	(select max(budget)
	from department)
select department.name
from department, max_budget
where department.budget = max_budget.value;



/* Complex Queries using With Clause */ 

-- Can have multiple queries in the with clause
	-- • Each one has a name
	-- • Each one has a list of attributes being returned
	-- • Can use attributes returned by other queries in the with clause
    
-- Find all departments where the total salary is greater than the average of the total salary at all departments
with dept_total (dept_name, value) as
	(select dept_name, sum(salary)
	from instructor
	group by dept_name),
dept_total_avg(value) as
	(select avg(value)
	from dept_total)
select dept_name
from dept_total, dept_total_avg
where dept_total.value > dept_total_avg.value;



/* Practice */ 
-- Find the maximum enrollment across all sections in Fall 2017. Use a WITH clause to do this.
with sec_enrollment as (
	select takes.course_id, takes.sec_id, count(ID) as enrollment
	from section, takes
	where takes.year = section.year
    and takes.course_id = section.course_id
	and takes.sec_id = section.sec_id
	and takes.semester = 'Fall'
	and takes.year = 2017
    group by takes.course_id, takes.sec_id)
select course_id, sec_id
from sec_enrollment
where enrollment = (select max(enrollment) from sec_enrollment);




/* Scalar Subquery in the Select Clause */

-- Scalar subquery is one which is used where a single value is expected
		-- • Can reference tables listed in the main query’s from clause
		-- • Can bring in its own list of tables in its own from clause
        
-- List all departments along with the number of instructors in each department
select dept_name,
		(select count(*)
		from instructor
		where department.dept_name = instructor.dept_name)
	as num_instructors
from department;
-- Runtime error if subquery returns more than one result tuple




/* 
Modification of the Database
§ Deletion of tuples from a given relation.
§ Insertion of new tuples into a given relation
§ Updating of values in some tuples in a given relation
*/




-- ------------------------------------- Deletion

-- Delete all instructors
delete from instructor;

-- Delete all instructors from the Finance department
delete from instructor
where dept_name= 'Finance';

-- Delete all tuples in the instructor relation for those instructors associated
-- with a department located in the Watson building.
delete from instructor
where dept_name in (select dept name
					from department
					where building = 'Watson');
-- Can use other set membership terms e.g. exists

-- Delete all instructors whose salary is less than the average salary of instructors
delete from instructor
where salary < (select avg (salary)
from instructor);

	/*
    • Problem: as we delete tuples from instructor, the average salary changes
	• Solution automatically used in SQL:
		1. First, compute avg (salary) and find all tuples to delete
		2. Next, delete all tuples found above (without recomputing avg or retesting the tuples)
	*/




-- ------------------------------------- Insertion
-- Add a new tuple to course
insert into course
values ('CS-437', 'Database Systems', 'Comp. Sci.', 4);

-- or equivalently
insert into course (course_id, title, dept_name, credits)
values ('CS-437', 'Database Systems', 'Comp. Sci.', 4);

-- Add a new tuple to student with tot_creds set to null
insert into student
values ('3003', 'Green', 'Finance', null);

-- Make each student in the Music department who has earned more than 144
-- credit hours an instructor in the Music department with a salary of $18,000.
insert into instructor
	select ID, name, dept_name, 18000
	from student
	where dept_name = 'Music' and total_cred > 144;

-- The select from where statement is evaluated fully before any of its results are inserted into the relation.
-- Otherwise queries like
insert into table1 select * from table1;
-- would cause problem




-- ------------------------------------- Updates
-- Give a 5% salary raise to all instructors
update instructor
set salary = salary * 1.05;

-- Give a 5% salary raise to those instructors who earn less than 70000
update instructor
set salary = salary * 1.05
where salary < 70000;

-- Give a 5% salary raise to instructors whose salary is less than average
update instructor
set salary = salary * 1.05
where salary < (select avg (salary)
				from instructor);
                
-- Increase salaries of instructors whose salary is over $100,000 by 3%, and
-- all others by a 5%
	-- • Write two update statements:
update instructor
	set salary = salary * 1.03
	where salary > 100000;

update instructor
	set salary = salary * 1.05
	where salary <= 100000;
-- The order is important						
-- Can be done better using the case statement \/

/* 
Case Statement for Conditional Updates 

case
	where predicate_1 then result_1
	where predicate_2 then result_2
	where predicate_3 then result_3
	…
	where predicate_n-1 then result_n-1
	else result_n
end
*/
-- Same query as before but with case statement
update instructor
	set salary = case
		when salary <= 100000 then salary * 1.05
		else salary * 1.03
		end;
        
/* Updates with Scalar Subqueries */ 

-- Recompute and update tot_creds value for all students
update student S
set tot_cred = (select sum(credits)
				from takes, course
				where S.ID= takes.ID and
					takes.course_id = course.course_id and
					takes.grade <> 'F' and
					takes.grade is not null);

-- Sets tot_creds to null for students who have not taken any course

-- To set tot_creds to 0 instead of null, could use another update to set null values to 0 or..

-- Instead of select sum(credits), we could use a case statement:
select case
	when sum(credits) is not null then sum(credits)
	else 0
end;


									/* End of Chapter 3!!!!!!!! */
        
        



