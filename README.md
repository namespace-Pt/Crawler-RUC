# Crawler-RUC
Several simple crawlers that can access [VRUC](vruc.edu.cn) and its subdomains with automatic captured cookies and tokens.

## Supported Feature
- [x] scrape your grades from http://jw.ruc.edu.cn
- [ ] automatically appoint to go out of school from http://appointment.ruc.edu.cn/

## Instruction
To use,
1. ```bash
   echo "student_id = 'your student id'" >> password.py
   echo "password = 'your password'" >> password.py
   ```
2. ```bash
   python main.py
   ```
   - currently, the main.py is used for retrieving all your grades and saving at `data/grades.json`
   - all crawlers are defined in `crawlers.py`

## Thanks
Thanks for [@邵总](https://github.com/rainym00d).