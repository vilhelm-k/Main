#%%
import yfinance as yf
import pandas as pd
import numpy as np
import time
import random


def get_data(ticker, startdate, enddate):
    data = yf.download(ticker, startdate, enddate)
    data['daily_returns'] = data['Close'].pct_change()
    data = data.dropna()
    return data

def getInterval(item, interval_list):
    return [idx for idx, value in enumerate(interval_list) if value <= item][-1]

def create_markov(data, N_OF_INTERVALS = 10):
    sortedData = sorted(data) # data får error för mig för att det inte är definierat. // Gustaf. 
                              # Svar: Alltså det är outputten får Eriks kod. En lista med procentuella ändringar, close to close //Ville

    entriesPerInterval = len(sortedData) / N_OF_INTERVALS
    intervals = [sortedData[round(i)] for i in np.arange(0, len(sortedData), entriesPerInterval)]

    # Gets midpoints to be used for random walk. Should prob be its own function but it is how it is 😂
    intervals.append(sortedData[-1])
    intervalMidpoints = [(intervals[i] + intervals[i + 1]) / 2 for i in range(len(intervals) - 1)]
    intervals.pop()

    # Creates 2d_list with all 0's
    markov_2d_list = [[0 for _ in range(N_OF_INTERVALS)] for _ in range(N_OF_INTERVALS)]

    # Loops through original data, adding 1 to each square where appropriate
    cur = getInterval(data[0], intervals)
    for entry in data[1:]:
        next = getInterval(entry, intervals)
        markov_2d_list[cur][next] += 1
        cur = next
    # returns tuple in form: (markovMatrix: List[List[float]], intervalMidpoints: List[float]). Both are same length
    return [[entry / sum(vector) for entry in vector] for vector in markov_2d_list], intervalMidpoints

def get_next_state(vector):
  total = sum(vector)
  r = random.uniform(0, total)
  upto = 0
  for idx, value in enumerate(vector):
      if upto + value >= r:
        return idx
      upto += value
  assert False, "Shouldn't get here"

def random_walk(markov_matrix, start_state, days, start_price, interval_midpoints):
  states = [start_state]
  prices = [start_price]
  for i in range(days):
    states.append(get_next_state(markov_matrix[states[-1]])) # saved for debugging
    prices.append(prices[-1] * (1 + interval_midpoints[states[-1]]))
  return states, prices

# Test functions
def avg_diff(true, predicted):
  return sum([abs(true[i] - predicted[i]) for i in range(len(true))]) / len(true)

def avg_percent_diff(true, predicted): # Done in a way such that +100% and -50% are equivalent
  return sum([fraction if (fraction := predicted[i] / true[i]) > 1 else 1 / fraction for i in range(len(true))]) / len(true)

def main():
  ticker = '^GSPC'
  start_train = '1990-01-08'
  end_train = '2016-06-23'
  start_test = '2016-06-23'
  end_test = '2022-12-08'
  matrix_size = 40
  number_of_runs = 10000
  extend_graph = False
  active_test = avg_percent_diff # Function used to compare simulations. Smaller value is better
  
  # initializes data
  data = get_data(ticker, start_train, end_test)
  daily_percentages = data['daily_returns'].squeeze()
  daily_prices = data['Close'].squeeze()
  train_percentages = daily_percentages[start_train : end_train]
  test_period_prices = daily_prices[start_test : end_test]

  # creates markov matrix
  markov_matrix, interval_midpoints = create_markov(train_percentages, matrix_size)    

  # sets up variables for random walk
  best_metric = None
  best_prediction = None
  random_prediction = None
  initial_state = getInterval(daily_percentages[start_test], interval_midpoints)
  
  start_time = time.time()
  diff_list = []
  # runs random walk number_of_runs times
  for i in range(1, number_of_runs + 1):
    if number_of_runs > 100:
      if i % round(number_of_runs / 10) == 0:
        print(i * 100 / number_of_runs, '% | est. time left:', round((time.time() - start_time) * (number_of_runs - i) / i), 's | best:', best_metric, end='\r')

    list_of_states, prices = random_walk(markov_matrix, initial_state, len(test_period_prices) - 1, test_period_prices[0], interval_midpoints)
    # print(list_of_states)
    # works out how close the prediction is to the actual values
    curr_metric = active_test(test_period_prices, prices)
    diff_list.append(prices)
    best_metric = best_metric if best_metric is not None else curr_metric # first run
    
    if curr_metric <= best_metric:
      best_metric = curr_metric
      best_prediction = prices
    
    random_prediction = prices

  avg = [sum(i) / len(i) for i in zip(*diff_list)]
  t = (avg[-1] / avg[0]) ** (1 / (len(avg)))
  print("average", t ** 251 - 1)
  print("best", active_test.__name__, (best_metric))
  print(f"Process finished in {round(time.time() - start_time)}s")
  
  display_prices = test_period_prices if not extend_graph else daily_prices
  prediction_prices = best_prediction if not extend_graph else [None] * (len(daily_prices) - len(best_prediction)) + best_prediction
  avg = avg if not extend_graph else [None] * (len(daily_prices) - len(avg)) + avg
  random_prediction = random_prediction if not extend_graph else [None] * (len(daily_prices) - len(random_prediction)) + random_prediction
  
  df = pd.DataFrame({"average prediction": avg, "random prediciton": random_prediction, "best prediction": prediction_prices, "real values": display_prices})
  graph = df['average prediction'].plot(color = ['#71bda7', '#c185c9', '#bdaf71', '#ED7E79'])

if __name__ == '__main__':
  main()
# %%
