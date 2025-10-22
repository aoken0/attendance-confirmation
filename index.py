import pandas as pd
import re

def build_page(csv_path, output_path):
  df = pd.read_csv(csv_path, header=None)
  # 頭から空列を削除
  col_del = []
  for col in df.columns:
    if df[col].isnull().all():
      col_del.append(col)
    else: break
  # 末尾から空列を削除
  for col in reversed(df.columns):
    if df[col].isnull().all():
      col_del.append(col)
    else: break
  # 両端の空列削除
  df = df.drop(columns=col_del).fillna("")
  
  # 座席表
  html_seats = '<div class="seats"><h1>座席表</h1><table>\n'
  regex = re.compile('[0-9]{2}[a-zA-Z]{1}[0-9]{4}')
  for l in df.values:
    no_match = not any(regex.search(e) for e in l)
    not_empty = any(l)
    if no_match and not_empty:
      html_seats += '\n</table>\n<table>\n'
      html_seats += '<tr>'
      for e in l:
        if not e:
          html_seats += '<td class="empty"></td>'
          continue
        html_seats += f'<td class="others">{e}</td>'
      html_seats += '</tr></table>\n<table>\n'
      continue

    html_seats += '<tr>'
    e: str
    for e in l:
      if not e:
        html_seats += '<td class="empty"></td>'
        continue
      if e.find('\n') >= 0:
        replaced_e = e.replace("\n", "<br>")
      else:
        replaced_e = re.sub(r'[\s\u3000]+', "<br>", e, count=1)
      html_seats += f'<td onclick="handleClick(this)">{replaced_e}</td>'
    html_seats += '</tr>\n'
  html_seats += '</table></div>\n'

  # 出席情報
  students = []
  for l in df.values.tolist():
    for e in l:
      if not e: continue
      if regex.search(e):
        tmp = regex.split(e)
        tmp.remove('')
        name = tmp[0].lstrip()
        students.append([regex.search(e).group(), name])
  sorted_students = sorted(students)
  html_sheet1 = '<table>\n<tr align="left"><th>名前</th><th>学籍番号</th></tr>\n'
  html_sheet2 = '<table>\n<tr align="left"><th>出席</th></tr>\n'
  for student in sorted_students:
    html_sheet1 += f'<tr><td>{student[1]}</td><td>{student[0]}</td></tr>\n'
    html_sheet2 += f'<tr><td align="right" width="32px" id={student[0]}>0</td></tr>\n'
  html_sheet1 += '</table>\n'
  html_sheet2 += '</table>\n'
  
  # テンプレートを読み込み
  with open('./template/template.html', 'r', encoding='utf-8') as f:
    html = f.readlines()
  insert_position = html.index('<main>\n') + 1
  
  # 座席表，出欠表を挿入
  html_content = html_seats + '<div><h1>名簿</h1><div class="attend-sheet">\n' + html_sheet1 + html_sheet2 + '</div></div>'
  html.insert(insert_position, html_content)
  with open(output_path, 'w', encoding='utf-8') as f:
    f.writelines(html)

if __name__ == '__main__':
  build_page('./csv/template.csv', './template.html')