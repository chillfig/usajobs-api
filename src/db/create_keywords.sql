CREATE TABLE IF NOT EXISTS keywords (
                                positionId int, 
                                positionTitle text,
                                orgName text, 
                                publishDate text, 
                                keywordQuery text,  
                                startingSalary real,
                                salaryInterval text, 
                                salaryMultiplier real, 
                                UNIQUE (positionId, keywordQuery) ON CONFLICT IGNORE
                                );