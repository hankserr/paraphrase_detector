def good_dates_dataset(good_dates):
  i = 0
  new_pairs = []
  last = good_dates[0][1]
  while i < len(good_dates) - 1:
    if good_dates[i][0] == good_dates[i+1][0]:
      new_pairs.append([good_dates[i][1], good_dates[i+1][1]])
      last = good_dates[i+1][1]
      i += 1
    elif good_dates[i][1] != last:
      new_pairs.append([last, good_dates[i][1]])
      last = good_dates[i+1][1]
    i += 1
  return new_pairs

a = [
  ['a', 1],
  ['a', 2],
  ['a', 3],
  ['b', 4],
  ['b', 5],
  ['b', 6],
  ['c', 7],
  ['c', 8],
  ['c', 9],
  ['c', 10]
]
