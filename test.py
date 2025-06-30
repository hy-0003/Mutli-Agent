import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.colors import ListedColormap
from typing import Tuple, List, Union

class EpidemicModels:
    def __init__(self, beta: float = 0.3, gamma: float = 0.1, sigma: float = 0.2,
                 N: int = 1000, days: int = 160, network_size: int = 200):
        # 基本参数默认值
        self.beta = beta    # 接触率
        self.gamma = gamma  # 恢复率
        self.sigma = sigma  # 潜伏期转化率
        self.N = N         # 总人口
        self.days = days   # 模拟天数
        self.network_size = network_size  # 网络节点数

    def sir_model(self, y: List[float], t: np.ndarray, beta: float, gamma: float, N: int) -> List[float]:
        S, I, R = y
        dSdt = -beta * S * I / N
        dIdt = beta * S * I / N - gamma * I
        dRdt = gamma * I
        return [dSdt, dIdt, dRdt]

    def seir_model(self, y: List[float], t: np.ndarray, beta: float, gamma: float, sigma: float, N: int) -> List[float]:
        S, E, I, R = y
        dSdt = -beta * S * I / N
        dEdt = beta * S * I / N - sigma * E
        dIdt = sigma * E - gamma * I
        dRdt = gamma * I
        return [dSdt, dEdt, dIdt, dRdt]

    def network_simulation(self, graph_type: str = 'watts_strogatz', steps: int = 50) -> Tuple[nx.Graph, np.ndarray]:
        """不同网络结构上的传播模拟"""
        valid_graph_types = ['watts_strogatz', 'barabasi_albert', 'random']
        if graph_type not in valid_graph_types:
            raise ValueError(f"Invalid graph type. Must be one of {valid_graph_types}")

        if graph_type == 'watts_strogatz':
            G = nx.watts_strogatz_graph(self.network_size, 4, 0.3)
        elif graph_type == 'barabasi_albert':
            G = nx.barabasi_albert_graph(self.network_size, 2)
        else:
            G = nx.erdos_renyi_graph(self.network_size, 0.05)

        # 初始化节点状态 (0=易感, 1=感染, 2=康复)
        status = np.zeros(self.network_size)
        patient_zero = np.random.randint(0, self.network_size)
        status[patient_zero] = 1

        # 模拟传播过程
        history = []
        for _ in range(steps):  # 模拟指定时间步
            new_status = status.copy()
            for node in range(self.network_size):
                if status[node] == 1:  # 感染节点
                    neighbors = list(G.neighbors(node))
                    for neighbor in neighbors:
                        if status[neighbor] == 0 and np.random.rand() < self.beta:
                            new_status[neighbor] = 1
                    if np.random.rand() < self.gamma:
                        new_status[node] = 2
            status = new_status
            history.append(status.copy())

        return G, np.array(history)

    def plot_results(self, t: np.ndarray, solutions: np.ndarray, model_type: str = 'SIR') -> None:
        plt.figure(figsize=(12, 6))
        if model_type == 'SIR':
            S, I, R = solutions.T
            plt.plot(t, S, label='Susceptible')
            plt.plot(t, I, label='Infected')
            plt.plot(t, R, label='Recovered')
        else:
            S, E, I, R = solutions.T
            plt.plot(t, S, label='Susceptible')
            plt.plot(t, E, label='Exposed')
            plt.plot(t, I, label='Infected')
            plt.plot(t, R, label='Recovered')

        plt.xlabel('Days')
        plt.ylabel('Population')
        plt.title(f'{model_type} Model Simulation')
        plt.legend()
        plt.grid()
        plt.show()

    def plot_network(self, G: nx.Graph, history: np.ndarray, step: int = -1) -> None:
        """可视化网络传播过程"""
        if len(history) == 0:
            raise ValueError("History data is empty")

        step = min(step, len(history)-1)  # 确保不越界
        plt.figure(figsize=(10, 8))
        colors = ListedColormap(['green', 'red', 'blue'])  # 易感, 感染, 康复
        pos = nx.spring_layout(G)
        nx.draw(G, pos, node_color=history[step], cmap=colors,
                node_size=50, with_labels=False)
        plt.title(f'Network Spread at Step {step}')
        plt.show()

    def run_sir_simulation(self) -> None:
        # 初始条件: 1个感染者, 其余易感
        I0 = 1
        S0 = self.N - I0
        R0_initial = 0
        y0 = [S0, I0, R0_initial]

        # 时间点
        t = np.linspace(0, self.days, self.days)

        # 解SIR模型
        solution = odeint(self.sir_model, y0, t, args=(self.beta, self.gamma, self.N))
        self.plot_results(t, solution, 'SIR')

        # 计算基本再生数R0
        basic_R0 = self.beta / self.gamma
        print(f"Basic Reproduction Number R0 = {basic_R0:.2f}")

    def run_seir_simulation(self) -> None:
        # 初始条件
        I0 = 1
        E0 = 0
        S0 = self.N - I0 - E0
        R0_initial = 0
        y0 = [S0, E0, I0, R0_initial]

        t = np.linspace(0, self.days, self.days)
        solution = odeint(self.seir_model, y0, t, args=(self.beta, self.gamma, self.sigma, self.N))
        self.plot_results(t, solution, 'SEIR')

        # 计算潜伏期影响
        print(f"Latent period = {1/self.sigma:.1f} days")

    def run_network_simulation(self, graph_type: str = 'watts_strogatz') -> None:
        try:
            G, history = self.network_simulation(graph_type)
            self.plot_network(G, history)

            if len(history) == 0:
                print("No simulation results to display")
                return

            # 计算传播范围
            final_infected = np.sum(history[-1] == 1)
            final_recovered = np.sum(history[-1] == 2)
            print(f"Final infected: {final_infected} ({final_infected/self.network_size:.1%})")
            print(f"Final recovered: {final_recovered} ({final_recovered/self.network_size:.1%})")
        except Exception as e:
            print(f"Network simulation failed: {str(e)}")

if __name__ == "__main__":
    try:
        model = EpidemicModels()

        print("=== SIR Model Simulation ===")
        model.run_sir_simulation()

        print("\n=== SEIR Model Simulation ===")
        model.run_seir_simulation()

        print("\n=== Network Spread Simulation (Watts-Strogatz) ===")
        model.run_network_simulation('watts_strogatz')

        print("\n=== Network Spread Simulation (Barabasi-Albert) ===")
        model.run_network_simulation('barabasi_albert')

        print("\n=== Network Spread Simulation (Random) ===")
        model.run_network_simulation('random')
    except Exception as e:
        print(f"Simulation error: {str(e)}")