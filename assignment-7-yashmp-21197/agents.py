from abc import abstractmethod
import numpy as np


class Agent(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Agent_" + self.name

    @abstractmethod
    def will_buy(self, value, price, prob):
        """Given a value, price, and prob of Junk,
        return True if you want to buy it; False otherwise.
        Override this method."""


class HalfProbAgent(Agent):
    """Buys if the prob < 0.5 no matter what the value or price is"""

    def will_buy(self, value, price, prob):
        return (prob < 0.5)


class RatioAgent(Agent):
    """Buys if the ratio of the price to value is below a specified threshold"""

    def __init__(self, name, max_p_v_ratio):
        super(RatioAgent, self).__init__(name)
        self.max_p_v_ratio = max_p_v_ratio

    def will_buy(self, value, price, prob):
        return (price / value <= self.max_p_v_ratio)


class BuyAllAgent(Agent):
    """Simply buys all products"""

    def will_buy(self, value, price, prob):
        return True


class StudentAgent(Agent):
    """The Student Agent"""

    def __init__(self, name):
        super(StudentAgent, self).__init__(name)
        # initialize both variable as zero.
        self.total_predicted_junk_probability = 0.0
        self.total_product_count = 0

    def will_buy(self, value, price, prob):
        # add this product in total product count
        self.total_product_count += 1
        # add current product's junk probability in total junk probability
        self.total_predicted_junk_probability += prob
        # take average of all products' junk probability as threshold
        average_junk_probability = self.total_predicted_junk_probability / self.total_product_count
        # result1 gives us an answer like ProbAgent with custom threshold which is average junk probability
        result1 = prob <= average_junk_probability
        price_to_value_ratio = price / value
        # increase the chance of selecting a product by taking complement of multiplication of average junk
        # probability and junk probability of a current product as threshold.
        # if junk probability is higher then chance of selecting of that product is lower and
        # if junk probability is lower than chance of selecting of that product is higher
        increase_selecting_chance = 1 - (average_junk_probability * prob)
        # result2 gives us an answer like RatioAgent with custom threshold which is fraction of junk probability
        result2 = price_to_value_ratio <= increase_selecting_chance
        return result1 and result2
