
-- creating sport table 
create table sport(
sport_ID char(5),
name varchar(20) not null,
gender char(2),
season varchar(6),
primary key(sport_ID))

-- Find the names of all instructors who have taught some course and the course_id
select name, course_id
from instructor , teaches
where instructor.ID = teaches.ID;

-- Find the names of all instructors in the Art department who have taught some course and the course_id
select name, course_id 
from instructor , teaches
where instructor.ID = teaches.ID
	and instructor. dept_name = 'Art';
    
-- Find the titles of courses in the Comp. Sci. department that have 3 credits
select title, course_id
from course
where dept_name = 'Comp. Sci.'
	and credits = 3

-- Get a nonredundant list of IDs of all students who were taught by an instructor named Einstein
select S.ID
from student as S, takes as T, teaches as TE, instructor as I
where S.ID = T.ID
	and T.course_id = TE.course_id
	and TE.ID = I.ID
    and I.name = 'Einstein'
-- OR
select t.ID
from takes t, teaches te, instructor i
where t.course_id = te.course_id
	and t.sec_id = te.sec_id
	and t.semester = te.semester
	and t.year = te.year
	and te.ID = i.ID
	and i.name = 'Einstein'

-- Get a nonredundant list of the names of students and the buildings that they have a class in
select st.name, s.building
from student st, takes t, section s
where st.id = t.id
	and t.sec_id = s.sec_id
	and t.semester = s.semester
	and t.year = s.year


/*
LECTURE 4
*/

-- PRACTICE
-- Find all students whose name starts with “S”
select student.name
from student
where student.name like 'S%'

-- Find all students whose name ends with “z”
select st.name
from student st
where st.name like '%z'

-- Find all students whose name has an “a” in the middle of their name (not at the start or end)
select st.name
from student st
where st.name like '%a%'

-- Find all students whose name has an “a” at the third position in their name
select st.name
from student st
where st.name like '__a%'
-- 




-- 
-- ORDER BY
-- 
select *
from instructor

select id, name
from instructor
order by name

select id
from instructor
order by name
-- 



-- 
-- Where Clause: Between
-- 
-- $90,000 and $100,000 (that is, >= $90,000 and <= $100,000)
select name
from instructor
where salary >= 90000 and salary <= 100000
-- Can write as:
select name
from instructor
where salary between 90000 and 100000
-- 

-- 
-- Where Clause: Compare Tuples
-- 
-- To simply things, we can compare tuples
select name, course_id
from instructor, teaches
where instructor.ID = teaches.ID and dept_name = 'Biology'
-- can be written as
select name, course_id
from instructor, teaches
where (instructor.ID, dept_name) = (teaches.ID, 'Biology')
--




-- 
-- Set Operations: union, intersect, except
-- 
-- Find courses that ran in Fall 2017 or in Spring 2018
(select course_id from section where sem = 'Fall' and year = 2017)
union
(select course_id from section where sem = 'Spring' and year = 2018)

-- Find courses that ran in Fall 2017 and in Spring 2018
(select course_id from section where sem = 'Fall' and year = 2017)
intersect
(select course_id from section where sem = 'Spring' and year = 2018)

-- Find courses that ran in Fall 2017 but not in Spring 2018
(select course_id from section where sem = 'Fall' and year = 2017)
except
(select course_id from section where sem = 'Spring' and year = 2018)
-- 

-- 
-- Practice: Set Operations
-- 
-- Select all entries from course sorted by title
select *
from course
order by title

-- Select all entries from course for Biology and Comp. Sci. using a union
-- (select using Biology union select using Comp. Sci.)
(select *
from course
where dept_name = 'Biology')
union
(select *
from course
where dept_name = 'Comp. Sci.')

-- Select all entries from section to find the courses taught in Packard in the
-- Spring using intersect (select using Spring intersect select using Packard)
(select *
from section
where semester = 'Spring')
intersect
(select *
from section
where building = 'Packard')
-- 




-- 
-- Aggregate Functions Examples
-- 
-- Find the average salary of instructors in the Computer Science department
select avg (salary)
from instructor
where dept_name= 'Comp. Sci.'

-- Find the total number of instructors who teach a course in the Spring 2018 semester
select count (distinct ID)
from teaches
where semester = 'Spring' and year = 2018
-- Note: Not allowed to use distinct * with count, but can use count(*)

-- Find the number of tuples in the course relation
select count (*)
from course

-- Aggregate Functions – Group By
-- Find the average salary of instructors in each department
select dept_name, avg (salary) as avg_salary
from instructor
group by dept_name;

/*
Group by attributes must appear in the select clause, and not in an aggregation function
Aggregation function must be in the select clause
Attributes in select clause outside of aggregate functions must appear in group by list (e.g. ID in this example)
*/
-- erroneous query
select dept_name, ID, avg (salary)
from instructor
group by dept_name;
-- where predicates are applied before the groups are formed

-- Aggregate Functions – Having Clause
-- Find the names and average salaries of all departments whose average salary is greater than 42000
select dept_name, avg (salary) as avg_salary
from instructor
group by dept_name
having avg (salary) > 42000
-- Note: predicates in the having clause are applied after the formation of groups 
-- (remember, predicates in the where clause are applied before forming groups)

-- Practice: Aggregation and Grouping
-- Using the course table, count the number of classes for each department.
-- Sort the output by department name in descending order
select dept_name, count(title)
from course 
group by dept_name
order by dept_name desc

insert into course(course_id, title, dept_name, credits)
values ('CS-001', 'Weekly Seminar', 'Comp. Sci.', 1);

delete from advisor where s_id = '12345';
delete from takes where ID = '12345';
delete from student where ID = '12345';

select distinct s.ID, s.name
from student s, takes t
where t.course_id like 'CS%'

select dept_name, max(salary)
from instructor
group by dept_name

select distinct s.ID, t.course_id
from student s, takes t
having count(t.course_id) >= 3
group by t.course_id

select distinct c.course_id, c.title
from course c, section s, time_slot ts
where c.course_id like 'CS%' and ts.end_hr >= 12 

select distinct t.course_id, t.ID
from takes t
where t.course_id in (select course_id
from takes
group by course_id, ID
having COUNT(*) >= 3)
order by t.course_id, t.ID;

select distinct t.course_id, t.ID
from takes t
group by t.course_id, t.ID
having COUNT(*) >= 3
order by t.course_id, t.ID;


select s.course_id, s.sec_id, s.year, s.semester, COUNT(t.ID)
from section s, takes t
where t.course_id = s.course_id;

select course_id, sec_id, year, semester, COUNT(*) as num
from takes
group by course_id, sec_id, year, semester
having COUNT(*) > 0;



-- calculateds how number of enrolled students are in each section
with enrollment as (
    select c.course_id, s.sec_id, s.year, s.semester, count(*) as num
    from course c, section s, takes t
    where c.course_id = s.course_id
        and s.course_id = t.course_id
        and s.sec_id = t.sec_id
        and s.year = t.year
        and s.semester = t.semester
    group by c.course_id, s.sec_id, s.year, s.semester)
-- selects the section with the most students enrolled
select se.course_id, se.sec_id, se.year, se.semester, se.num
from enrollment se
where se.num = (select max(num) from enrollment);


select s.ID, s.name
from student s, takes t, course c
where s.ID = t.ID
    and s.dept_name = 'Music'
    and s.name like 'S%'
    and t.course_id = c.course_id
    and c.dept_name = 'Comp. Sci.'
group by s.ID, s.name
having count(distinct t.course_id) = 5;

-- This returns nothing because there is only one student who is a music major
-- This following query shows that it works:

select s.ID, s.name
from student s, takes t, course c
where s.ID = t.ID
    and s.dept_name = 'Music'
    and s.name like 'S%'
    and t.course_id = c.course_id
    and c.dept_name = 'Music' -- (this student only takes a music course)
group by s.ID, s.name
having count(distinct t.course_id) = 1; -- (this studnet only takes one course)
-- query returns ID, name: (55739, Sanchez)

select s.ID
from student s
left join takes t on s.ID = t.ID
where t.ID is null;



