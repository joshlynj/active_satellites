## 🌌 Satellite Life Expectancy 

## 💼 Stakeholder Interest
Knowing about what affects the life of a satellite allows for better mission planning, including scheduling replacements or adjustments to ensure continuous and reliable satellite coverage.
Understanding the factors that affect satellite lifetimes, such as orbit type, can help the military allocate resources effectively by choosing the most suitable orbits for different types of missions. 
Satellites play a crucial role in maintaining situational awareness, command and control, and communication during various operations. Knowing which orbits provide longer lifetimes can contribute to more reliable and sustained operations.
Satellite development, launch, and maintenance are extremely costly. By understanding factors that influence satellite longevity, the military can make informed decisions about investment in satellite technology, design, and orbits to optimize the cost-effectiveness of their satellite programs.
Space situational awareness, which involves monitoring and tracking objects in space, helps to prevent collisions and protect satellites from potential threats. Knowledge of satellite lifetimes can aid in predicting end-of-life scenarios and potential debris creation.

## ☄ Data of Interest
- Expected Lifetime (Years)
- Launch Mass (Kilograms)
- Inclination (Degrees)
- Apogee (Kilometers)
- Perigee (Kilometers)
- Class of Orbit

## 🤓 Data Wrangling
The majority of the issues were in the expected lifetime column. Some of the data was in ranges while others were just a specific number. To tackle this issue, I replaced the range with the mean. 
I also had to create dummy variables for class of orbit as it was one categorical column. Creating the dummy variables allowed me to make comparisons between how the different orbits behaved. 
There were null values in both the expected lifetime column and in the launch mass column, so I deleted the null rows to avoid any complications with the data. 

## 🔬 Hypotheses
H0 : Satellites in GEO will have a similar life expectancy compared to those in other orbits                   
H1 : Satellites in GEO will have a longer life expectancy compared to those in other orbits             

## 🧪 Hypotheses Testing
![image](https://github.com/joshlynj/active_satellites/assets/96899068/37143179-f237-4a8a-ac53-5ca8cce17e71)           
I decided to use an ANOVA test for my hypothesis as it allowed me to determine whether the means of the life expectancy for each orbit were significantly different from each other.        
This test compares the variability within each orbit to the variability between the orbits and calculates a test statistic and p-value to assess the significance of the differences.   
In this test, I set my significance level to 0.05 which means that if the p-value is greater than 0.05 then we do not have enough evidence to reject the null hypothesis.     
In this case, our P value is significantly smaller than 0.05 which means that we can reject the null hypothesis, proving that satellites in GEO have a longer life expectancy than those in other orbits.           
I also used a Tukey HSD after completing the ANOVA test which shows the specific comparison between each group. It shows the mean difference in years 



## 🛰 Average Lifetime of Satellites vs. Orbit
![image](https://github.com/joshlynj/active_satellites/assets/96899068/1165e4f1-807f-4df7-b893-19e58733d54d)
Here is a visual representation that shows the average life-time of a satellite based on years.
As you can see GEO has the highest life expectancy whereas elliptical has the lowest life expectancy. 


## 📡Linear Regression Model
- Perigee (Kilometers) 
- Apogee (Kilometers)
- Launch Mass (Kilograms)
- Inclination (Degrees)

I chose to use perigee and apogee instead of the orbits as these are numerical values instead of categorical. This provided my model with higher accuracy. 

![image](https://github.com/joshlynj/active_satellites/assets/96899068/127bfd18-45cb-456c-8942-46185ae7acb2)

The regression analysis conducted on the dataset provides valuable insights into the relationship and their expected lifetimes.      
between satellite characteristics           
The model, based on the Ordinary Least Squares (OLS) method, demonstrates a reasonable fit to the data with an R-squared value of 0.604, indicating that approximately 60.4% of the variance in the expected lifetime of satellites is explained by the chosen predictor variables.              

The F-statistic of 361.3 and associated low probability value (p-value) affirm the overall significance of the regression, implying that the model as a whole is meaningful.  
        
![image](https://github.com/joshlynj/active_satellites/assets/96899068/9d92057f-ff86-4192-9f89-c549af8cfd3e)          


## 🌠 Original Dataset
https://www.kaggle.com/datasets/ucsusa/active-satellites
