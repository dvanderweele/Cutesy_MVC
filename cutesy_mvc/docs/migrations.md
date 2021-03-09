# Migration File Format

## Filename Parts 

0 - TYPE: create, edit, drop (note that edit table migrations do not support operations other than renaming things)
1 - NAME: table name 
2 - TIMESTAMP: unix timestamp from migration file generation time, hyphenated format of floating point value
3 - SUFFIX: file ending, i.e. mign

## Two Major Sections

Demarcated by by "UP" on line 1, and then "DOWN" on line 3 or greater. 

## 5 Types of Lines

### col 

3 parts, separated by tilde ~

```
col~[columnName]~[columnSpecifier]
```

columnName is the name of the column to be created.

columnSpecifier is the details about the column, like what you would put in an sqlite create table query to describe the column.

examples: 

```
col~id~INTEGER PRIMARY KEY NOT NULL
col~name~TEXT
col~price~REAL
```

### comp 

indicates a composite primary key specification. after comp~ list column names, separated by commas, to indicate which columns make up the composite key.

example:
```
col~building~INTEGER NOT NULL
col~room~INTEGER NOT NULL
comp~building,room
```

### foreign 

specify one foreign key per line. Four parts to a line, separated by tildes. From the left, first part is keyword foreign, then in the position after that is name of column in this table that will be a foreign key, next is the foreign table name, and finally is the column name in the foreign table referenced by the foreign key.

example:
```
foreign~cohortId~cohort~id 
```

### timestamps

only one word required on this line, and that is "timestamps". Will create created_at and updated_at columns for table automatically. 

example:
```
timestamps 
```

### drop-table
only one word required on this line, and that is "drop-table". When present in an UP or DOWN section, typically the only line in that section. Intended to be the reverse of the creation operations specified in the opposite section of the migration file.

### Example File:

filename: create.user.1234332235-23424.mign

contents:
```
UP 
col~id~INTEGER PRIMARY KEY NOT NULL
col~name~TEXT NOT NULL
col~groupId~INTEGER
foreign~groupId~group~id
DOWN
drop-table
```

### Edit/Alter Table Files

Only one operation is directly supported: renaming a table. Up and Down sections work as above. Unfortunately renaming columns isn't even supported because it is not supported in all versions of sqlite you are likely to encounter out in the wild so... you will have to manually emulate alter table functionality such as renaming columns and adding columns by methods such as creating new tables, moving data over, and renaming the new table.

#### rntab - 3 fields

From the left, fields separated by colons: first field is rntab keyword, second field is old tablename, third field is new tablename.

```
rntab:users:user
```

#### Example Edit File

filename: edit.users.1234334435-23424.mign

contents:
```
UP
rntab:user:users
DOWN
rntab:users:user
```