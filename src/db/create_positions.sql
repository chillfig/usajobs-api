CREATE TABLE IF NOT EXISTS positions (
                                positionId int, 
                                positionTitle text,
                                orgName text, 
                                publishDate text, 
                                positionQuery text,  
                                startingSalary real,
                                salaryInterval text, 
                                salaryMultiplier real, 
                                UNIQUE (positionId, positionQuery) ON CONFLICT IGNORE
                                );