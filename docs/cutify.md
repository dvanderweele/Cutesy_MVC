## `cutify` Command-Line Tool Usage 

Following examples assume project is in folder called 'cutesy'.

Run all outstanding migrations:

```
python -m cutesy cutify migrate
```

Rollback last batch of migrations (i.e. by running each of the DOWN operations from those migrations):

```
python -m cutesy cutify rollback-migrations 
```

Generate a fresh migration file. <type> can be either create, edit, or delete. One table per migration file:

```
python -m cutesy cutify make:migration:<type>:<table name>
```

Display the schema (i.e. table names and their columns) for the current database as specified in configuration:

```
python -m cutesy cutify db:schema
```

Delete the current database file as specified in configuration if it exists, and then create a new one and run the migrate command:

```
python -m cutesy cutify db:refresh
```

You can use the tool to auto-generate `model` and `controller` file boilerplate. 

```
python -m cutesy cutify make:model:User
python -m cutesy cutify make:controller:UserController
```

You can use the tool to run all of your tests:

```
python -m cutesy cutify test
```
