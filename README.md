# Simple Global TFR Analysis
This code provides an introduction to ML using scikit-learn and statsmodels by using an Ordinary Least Squares (OLS) linear regression to examine the influence certain economic, demographic, and cultural factors can have over a country's Total Fertility Rate using a combination of log, dummy, and numeric variables. 

## Data Sources
- **UN Population Division (2024)**: TFR and teen birth rates.
- **World Bank**: GDP per capita (https://data.worldbank.org/indicator/NY.GDP.PCAP.CD) and female labor force participation (https://data.worldbank.org/indicator/SL.TLF.CACT.FE.ZS)
- **Custom Dataset**: `variables_2.csv` includes cultural dummies (e.g., SSA, East Asia)—feel free to edit categorizations.
All data is for 2023.

## Methods
### Female Workforce Participation and GDP Per Capita
The first regression uses the two variables most cited to have an effect on TFR: GDP per capita and women's workforce participation. I use a log of GDP per capita because of the large disparity in individual income between rich and poor countries- compare Angola, with a yearly GDP per capita of $2309, with Sweden, which has $55567. I found that using the logged version of female workforce participation was not necessary- there is enough of a linear trend across countries. The covariance between these two variables was low. At least according to the World Bank Data, low income countries can also have high female workforce participation. The results showed that when GDP per capita is controlled for, female workforce participation actually has a positive effect compared to the strongly negative effect of country wealth.

### Add Teen Births Per Capita
After this I added in births between the ages of 15 and 19 per capita, accounting for the fact that historically, many births were incidental before the normalization of birth control. The 'Births by women aged 15 to 19 (per capita)' is a variable I added into the original dataset, but can be calculated independently. Once again, I used a log due to the large disparity between low income and high income countries. The covariance between teen births and GDP per capita was high, a little above 3 each, which makes sense, since poorer countries tend to have less education around birth control and safe sex. The results showed that the teen birth variable had a significant positive effect on TFR, and made female workforce participation much less significant.

### Add cultural dummies
Finally, for the third regression I add in a cultural factor, to test the hypothesis that outlook on child rearing is at least partially cultural. I create several dummy (binary) variables to signify a country's place in one of several cultural "regions": Sub Saharan Africa, the East Asian Buddhist/Hindu countries, the non-SSA Muslim countries, Europe and the West, and Latin America. The covariance between teen births and GDP per capita becomes even higher, which may be holding the accuracy of the regression back. Nevertheless, the results show visible significance for most of the five regions (in the final third regression I keep Europe and the West out because it shows a negligible effect.) The final result should show a 0.763 R2, with below 0.2 P>|t| for all variables, with Sub Saharan Africa and non-SSA Muslim cultures encouraging large families even after controlling for income, female workforce participation, and teen birth, and East Asia and Latin America discouraging them.

I may add additional variables such as average college education and irreligon to see if they have a factor as well, presuming that they don't show too great covariance with country wealth. But in the meantime, this study provides a statistical lens into what would otherwise be a complex socioeconomical subject.
