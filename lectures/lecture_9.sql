# Lecture 9

/*
Declaring SQL Functions
§ Define a function that, given the name of a department, returns the count of
the number of instructors in that department.
*/

create function dept_count (dept_name varchar(20))
	returns integer
	begin
	declare d_count integer;
		select count (*) into d_count
		from instructor
		where instructor.dept_name = dept_name
	return d_count;
end


/*
Table Functions
§ The SQL standard supports functions that can return tables as results; such
functions are called table functions
§ Example: Return all instructors in a given department
*/
create function instructor_of (dept_name char(20))
	returns table (
		ID varchar(5),
		name varchar(20),
		dept_name varchar(20),
		salary numeric(8,2))
	return table
		(select ID, name, dept_name, salary
		from instructor
		where instructor.dept_name = instructor_of.dept_name)

# Usage
select *
from table (instructor_of ('Music'))



/*
SQL Procedures
§ The dept_count function could instead be written as procedure:
*/
create procedure dept_count_proc (in dept_name varchar(20),
								out d_count integer)
	begin
		select count(*) into d_count
		from instructor
		where instructor.dept_name = dept_count_proc.dept_name
	end
/*    
§ The keywords in and out are parameters that are expected to have
values assigned to them and parameters whose values are set in the
procedure in order to return results.
§ Procedures can be invoked either from an SQL procedure or from
embedded SQL, using the call statement.
*/
declare d_count integer;
call dept_count_proc( 'Physics', d_count);




# MySQL Note
#§ General form:
create function funct_name (variables being passed in)
	returns whatever_it_is_returning DIRECTIVE_GOES_HERE
	begin
	declare variable_name_and_type_to_be_returned
		SQL statements
	return variable_name_to_be_returned;
end

#§ This example says that the function is reading data from a table
create function dept_count (dept_name varchar(20))
	returns integer READS SQL DATA
	begin
	declare d_count integer;
		select count (* ) into d_count
		from instructor
		where instructor.dept_name = dept_name
	return d_count;
end

/*
Important: Semi-colons conflict of meaning
Need to change the delimiter used for CREATE, and then change it back
delimiter whatever_you_want_it_to_be
*/
delimiter $$ 					# This changes the delimiter for CREATE to $$
	create function dept_count (dept_name varchar(20))
	returns integer
	begin
	declare d_count integer; 	# ; here is now ok
		select count (* ) into d_count
		from instructor
		where instructor.dept_name = dept_name
	return d_count; 			# ; here is now ok
end$$ 							# Note the $$ instead of the ;
delimiter ; 					# Changed the delimiter back to ;



/* 
Recursion in SQL
§ SQL:1999 permits recursive view definition
§ Example: find which courses are a prerequisite, whether directly or indirectly, for a
specific course
*/
with recursive rec_prereq(course_id, prereq_id) as (
		select course_id, prereq_id
		from prereq
	union
		select rec_prereq.course_id, prereq.prereq_id,
		from rec_prereq, prereq
		where rec_prereq.prereq_id = prereq.course_id
	)
select ∗
from rec_prereq;
# This example view, rec_prereq, is called the transitive closure of the prereq relation










