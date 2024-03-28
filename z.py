import re

text = """
var a = 1 /* комментарий */
/* много строчный
комментарий
*/
"""

# Удаление комментариев из строки
text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)

print(text)
