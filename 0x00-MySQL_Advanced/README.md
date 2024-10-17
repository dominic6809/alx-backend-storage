# 0x00-MySQL_Advanced

## 1. Creating Stored Procedures

### **Stored Procedure: ComputeAverageWeightedScoreForUsers**

- **Purpose**: Computes and stores the average weighted score for all users.
- **Input**: None.

### **Logic**:
- Use a cursor to iterate through each user in the `users` table.
- For each user:
  - Calculate the total weighted score and total weight using the `corrections` and `projects` tables.
  - Update the `average_score` in the `users` table based on the calculated values.

### **Key SQL Statements**:
- **Cursor**: 
  ```sql
  DECLARE user_cursor CURSOR FOR SELECT id FROM users;
  ````
  
  - **Fetch**
    ```
    FETCH user_cursor INTO userId;
    
  - **Calculation:**
    ```
      SELECT SUM(c.score * p.weight) INTO total_weighted_score,
          SUM(p.weight) INTO total_weight
      FROM corrections c
      JOIN projects p ON c.project_id = p.id
      WHERE c.user_id = userId;

- **Update**
  ```
    UPDATE users
    SET average_score = total_weighted_score / total_weight
    WHERE id = userId;

## 2. Initial Setup
### Database Schema:
#### Tables:
    users: Stores user information including id, name, and average_score.
    projects: Contains project details with id, name, and weight.
    corrections: Links users to their project scores with user_id, project_id, and score.

## Execution:
Run the SQL scripts to set up the environment and execute the stored procedure to observe the changes in average scores for all users.

## Conclusion
Understanding stored procedures and cursor usage is crucial for performing batch operations on database records.
This knowledge is essential for efficiently managing data in relational databases.
