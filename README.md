# reservoir-operation-Spark

Step1: Run main.py and Longin
user:SKDD
password:123456

Step2: Import Data
Import four types of data: reservoir name, basic curve, streamflow data, and control conditions through clicking the 'Select File' button. The data file template format is in the folder. The 'Reservoir' corresponds to importing the '[Demo] Reservoir.txt' file, the 'Curve' corresponds to importing the '[Demo] Curve.csv' file, the 'Streamflow' corresponds to importing the '[Demo] Streamflow.csv' file, and the 'Conditions' corresponds to importing the' [Demo] Condition.csv' file. 

Step3: Query Data
Query the imported data. The “Basic Curves” query displays the water level-storage capacity curve, tailwater level-flow curve, and water consumption rate curve of each reservoir in the form of scatter plots and tables. On the right side of the query interface, there is a dropdown box for users to select different reservoir names and basic curve names. Click the “Query” button to display the corresponding basic curve data of the selected reservoir.
The “Streamflow data” query displays the inflow (or interval) runoff process of each reservoir in the form of line charts and tables. On the right side of the query interface, there is a dropdown box for users to select different reservoir names. Click the “Query” button to display the corresponding inflow (or interval) runoff process of the selected reservoir.
The “Control Conditions” query displays the control parameters such as the maximum/minimum water level, maximum/minimum load of each reservoir in the form of a table. The upper part of the query interface is in the form of a drop-down box for users to select different reservoir names. Click the “Query” button to display the corresponding control condition information of the selected reservoir. The right box represents the two control boundaries for the starting and ending water levels of each reservoir.

Step 4: Set parameters
The “Parallel number” refers to the number of CPU cores used for parallel computing. For an 8-core computer, there are five options for setting the parallel number: 1, 2, 4, 6, and 8, as shown in Fig. 13. When the parallel number is set to 1, it means that only one CPU is involved in the calculation, that is, serial calculation; Only when the number of parallel is greater than 1, it is considered multi-core parallel computing.
The “Reservoirs in Optimizing” option allows for flexible setting of reservoirs that need to participate in optimization operation. After importing the “Reservoir” file, the checkbox for “Reservoirs in Optimizing” will automatically display the names of all reservoirs. Select the name of the reservoir that needs to participate in optimization.

Step 5: Spark-based parallel optimization
After clicking the “Calculate” button, the parallel optimization calculation will begin. After the calculation is completed, a prompt window will pop up with information about the calculation time.

Step 5: Display results
After parallel calculation is completed, click on the “Results” button, the operation plan results of each reservoir in a graphical form.
The water level, outflow, output, and energy yield process are decision-making indicators in actual operation, which will be displayed in the form of charts on the interface for a more intuitive view. On the right side of the results query interface, there is a dropdown box for users to select different reservoir names and query processes. Click the “Query” button to display the corresponding operation plan process for the selected reservoir.



