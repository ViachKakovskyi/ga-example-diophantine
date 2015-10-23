import unittest
from unittest import mock

import diophantine as dio


class DiophantineTestCase(unittest.TestCase):
    def setUp(self):
        self.instance = [0, 0]
        self.mocked_successful_population = [mock.Mock(fitness=fitness) for fitness in range(10, -1, -1)]
        self.not_successful_population = [[attribute, attribute] for attribute in range(10)]
        self.successful_population = self.not_successful_population + [dio.SOLUTION]

        self.assertNotIn(dio.SOLUTION, self.not_successful_population,
                         'Looks like `not_successful_population` is corrupted. You should check `dio.SOLUTION`.')

    def test_fitness(self):
        self.assertEqual((0, ), dio.fitness(dio.SOLUTION))

    def test_spawn_instance(self):
        for _ in range(0, 100):
            x, y = dio.spawn_instance()
            assert dio.MIN <= x <= dio.MAX
            assert dio.MIN <= y <= dio.MAX

    def test_mutate(self):
        self.assertEqual((self.instance, ), dio.mutate(self.instance, 0))
        self.assertNotEqual(self.instance, dio.mutate(self.instance, 1.1))

    def test_best_result(self):
        self.assertIs(self.mocked_successful_population[-1],
                      dio.get_best_result(self.mocked_successful_population))

    def test_terminate(self):
        self.assertFalse(dio.terminate(self.not_successful_population))
        self.assertRaises(StopIteration, dio.terminate, self.successful_population)

    def test_setup(self):
        # checks if no exceptions are raised
        toolbox = dio.setup(mutpb=0.5)

    def test_main(self):
        best_instance = dio.main(*dio.DEFAULT_MAIN_ARGS)
        self.assertEqual(dio.SOLUTION, best_instance,
                         'Try again, or configure the Genetic Algorithm properly')

    @mock.patch('builtins.print')
    def test_output(self, _print):
        dio.output(dio.SOLUTION)
        _print.assert_has_calls([mock.call(dio.BEST_INSTANCE_MSG, dio.SOLUTION)])

    @mock.patch('builtins.print')
    def test_output_no_solution(self, _print):
        dio.output(self.instance)
        _print.assert_has_calls([mock.call(dio.BEST_INSTANCE_MSG, self.instance),
                                mock.call(dio.NO_SOLUTION_MSG,
                                          dio.fitness(self.instance))])


if __name__ == '__main__':
    unittest.main()