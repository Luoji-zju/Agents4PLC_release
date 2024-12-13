## Description on benchmark construction

This is the version of code at the paper summit time. However, recently we have expanded our benchmark, 
which will be released later. The following presents the file for easy and medium level:

```
/easy.json
/medium.json
```

Current dataset comprises 23 programming tasks along with corresponding formal verification specifications, including 58 properties in easy set with 53 non-trivial property over 16 easy programming tasks and 43 in medium set with 38 non-trivial property over 7 medium programming tasks, where trivial property means ”assertion” property without corresponding assertion sentences in ST code for reference.

The standard of classification is designed as follows, despite the fact that the standard need expert assistance, and in out classification
some cases that originally classified to medium could be better is classified to hard: 

### Easy
The task involves only basic assignment operations and simple conditional checks (such as IF statements), which only uses simple data types (e.g., BOOL, INT). The process logic is simple, clear, and without nested structures. Neither complex external interface calls nor communication protocol handlings are required. This part of code are usually used as 
independent logic outside the core modules of the PLC system.

### Middle
The task includes multiple conditional statements or simple loop structures (e.g., FOR, WHILE). It requires basic data structures (e.g., arrays) and moderately complex variables. It involves interaction between multiple functional modules or program segments. Some basic exception handling or state management is needed. Includes simple interface communication with devices or sensors.

### Hard
The task contains complex nested logic, multiple conditional branches, and complex loops. It uses advanced data types (e.g., structures, enumerations) and complex data management. It involves complex inter-module communication and multithreading. It includes complex state machine design and real-time response logic. Advanced interface communication, such as large-scale data exchange with SCADA systems or other PLCs, is involved. There are high requirements for performance and reliability, requiring in-depth code optimization. It involves safety-critical system functions and requires strict error and exception handling.




This is a part of benchmark which can be directly used to test your multi-agent's implement.
/test.json