import re


def formatNum(num):
  if not num:
    raise TypeError('No number was provided.')
  isNeg = False
  if num[0] == '-':
    num = num[1:]
    isNeg = True
  if num[0] == '+':
    num = num[1:]
  if not re.match('\\d*\\.?\\d*', num).group():
    raise TypeError('Invalid number was provided.')
  num = re.sub('^0+', '', num)
  if '.' in num:
    num = re.sub('0+$', '', num)
  if num == '' or num == '.':
    num = '0'
  if num[0] == '.':
    num = '0' + num
  if num[-1] == '.':
    num = num[:len(num)-1]
  if num != '0' and isNeg:
    return '-'+num
  return num


def isSmaller(num1, num2):
  num1 = num1.split('.')
  num2 = num2.split('.')
  num1L = len(num1)
  num2L = len(num2)
  num1IL = len(num1[0])
  num2IL = len(num2[0])

  if num1IL > num2IL:
    return False
  if num1IL < num2IL:
    return True
  if num1IL == num2IL:
    for i in range(num1IL):
      if num1[0][i] > num2[0][i]:
        return False
      if num1[0][i] < num2[0][i]:
        return True
  if num1L == num2L == 1:
    return False
  if num1L == num2L == 2:
    if num1[1] < num2[1]:
      return True
    else:
      return False
  if num1L == 2:
    return False
  else:
    return True


def addition(num1, num2):
  if num1 == '0':
    return num2
  if num2 == '0':
    return num1
  isNeg = False
  if num1[0] == '-' and num2[0] == '-':
    isNeg = True
    num1 = num1[1:]
    num2 = num2[1:]
  elif num1[0] == '-' and num2[0] != '-':
    num1 = num1[1:]
    return subtraction(num2, num1)
  elif num1[0] != '-' and num2[0] == '-':
    num2 = num2[1:]
    return subtraction(num1, num2)
  deciPos1 = 0
  deciPos2 = 0
  if '.' in num1:
    deciPos1 = len(num1) - num1.find('.') - 1
    num1 = num1.replace('.', '', 1)
  if '.' in num2:
    deciPos2 = len(num2) - num2.find('.') - 1
    num2 = num2.replace('.', '', 1)
  if deciPos1 > deciPos2:
    for i in range(deciPos1-deciPos2):
      num2 = num2 + '0'
  if deciPos1 < deciPos2:
    for i in range(deciPos2-deciPos1):
      num1 = num1 + '0'
  res = str(int(num1)+int(num2))
  maxPos = max(deciPos1, deciPos2)
  if maxPos > 0:
    resL = len(res)
    res = res[:resL - maxPos] + '.' + res[resL - maxPos:]
  if isNeg:
    res = '-'+res
  return formatNum(res)


def subtraction(num1, num2):
  if num2 == '0':
    return num1
  if num1 == '0':
    if num2[0] == '-':
      return num2[1:]
    return '-'+num2

  if num1[0] == '-' and num2[0] == '-':
    num1 = num1[1:]
    num2 = num2[1:]
    [num1, num2] = [num2, num1]
  elif num1[0] == '-' and num2[0] != '-':
    return addition(num1, '-'+num2)
  elif num1[0] != '-' and num2[0] == '-':
    num2 = num2[1:]
    return addition(num1, num2)
  deciPos1 = 0
  deciPos2 = 0
  if '.' in num1:
    deciPos1 = len(num1) - num1.find('.') - 1
    num1 = num1.replace('.', '', 1)
  if '.' in num2:
    deciPos2 = len(num2) - num2.find('.') - 1
    num2 = num2.replace('.', '', 1)
  if deciPos1 > deciPos2:
    for i in range(deciPos1-deciPos2):
      num2 = num2 + '0'
  if deciPos1 < deciPos2:
    for i in range(deciPos2-deciPos1):
      num1 = num1 + '0'
  res = ''
  if isSmaller(num1, num2):
    res = '-'+str(int(num2)-int(num1))
  else:
    res = str(int(num1)-int(num2))
  maxPos = max(deciPos1, deciPos2)
  if maxPos > 0:
    resL = len(res)
    res = res[:resL - maxPos] + '.' + res[resL - maxPos:]
  return formatNum(res)


def multiplication(num1, num2):
  if num1 == '0' or num2 == '0':
    return '0'
  negCount = 0
  if num1[0] == '-':
    negCount += 1
    num1 = num1[1:]
  if num2[0] == '-':
    negCount += 1
    num2 = num2[1:]
  deciPos = 0
  if '.' in num1:
    deciPos += len(num1) - num1.find('.') - 1
    num1 = num1.replace('.', '', 1)
  if '.' in num2:
    deciPos += len(num2) - num2.find('.') - 1
    num2 = num2.replace('.', '', 1)
  res = str(int(num1)*int(num2))
  if deciPos > 0:
    if len(res) < deciPos:
      n = deciPos - len(res)
      for i in range(n):
        res = '0' + res
    resL = len(res)
    res = res[:resL - deciPos] + '.' + res[resL - deciPos:]
  if negCount == 1:
    res = '-'+res
  return formatNum(res)


def division(num1, n2, count=10):
  if num1 == '0':
    return '0'
  if n2 == '0':
    raise ZeroDivisionError('division by zero', num1+'/'+'0')
  negCount = 0
  if num1[0] == '-':
    negCount += 1
    num1 = num1[1:]
  if n2[0] == '-':
    negCount += 1
    n2 = n2[1:]
  deciPos = 0
  if '.' in num1:
    deciPos += len(num1) - num1.find('.') - 1
    num1 = re.sub('^0+', '', num1.replace('.', '', 1)) or '0'
  if '.' in n2:
    deciPos -= len(n2) - n2.find('.') - 1
    n2 = re.sub('^0+', '', n2.replace('.', '', 1)) or '0'
  n2M = []
  for i in range(1, 11):
    n2M.append(str(int(n2)*i))
  result = ''
  remain = ''
  deciAdded = False
  n2L = len(n2)
  selected = False

  while remain != '0' or num1:
    n1 = ''
    if remain != '0':
      n1 = remain
    AFN = False
    if not selected:
      selected = True
      if num1:
        n1 += num1[:n2L]
        num1 = num1[n2L:]
    while isSmaller(n1, n2):
      if AFN:
        result += '0'
      if not num1 and not n1:
        break
      if num1:
        n1 += num1[0]
        num1 = num1[1:]
        AFN = True
      else:
        count = count-1
        if count < 0:
          n1 = ''
          break
        if not deciAdded:
          deciAdded = True
          result += '.'
        n1 += '0'
        AFN = True
      n1 = re.sub('^0+', '', n1)
    if not n1:
      break
    for i in range(0, 10):
      got = n2M[i]
      if got == n1:
        remain = '0'
        result += str(i+1)
        break
      if not isSmaller(got, n1):
        result += str(i)
        remain = str(int(n1) - int(n2M[i-1]))
        break
  if deciPos:
    curr = 0
    spl = result.split('.')
    if len(spl) == 2:
      curr = len(spl[1])
    deciPos += curr
    if deciPos:
      result = result.replace('.', '', 1)
      resL = len(result)
      if deciPos > 0:
        if resL < deciPos:
          for i in range(deciPos-resL):
            result = '0'+result
          result = '.'+result
        else:
          result = result[:deciPos]+'.'+result[deciPos:]
      elif deciPos < 0:
        for i in range(abs(deciPos)):
          result += '0'
  if negCount == 1:
    result = '-'+result
  return formatNum(result)


class HM:
  def __init__(self, num):
    if type(num) != str:
      raise TypeError('Input number must be string. Not number.')
    self.result = formatNum(num)

  def add(self, num):
    if type(num) != str:
      raise TypeError('Input number must be string. Not number.')
    num = formatNum(num)
    self.result = addition(self.result, num)
    return self

  def sub(self, num):
    if type(num) != str:
      raise TypeError('Input number must be string. Not number.')
    self.result = subtraction(self.result, num)
    return self

  def multiply(self, num):
    if type(num) != str:
      raise TypeError('Input number must be string. Not number.')
    self.result = multiplication(self.result, num)
    return self

  def divide(self, num, count=10):
    if type(num) != str:
      raise TypeError('Input number must be string. Not number.')
    self.result = division(self.result, num, count)
    return self
