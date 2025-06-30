import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.linear_model import LinearRegression
import seaborn as sns

# 设置随机种子保证可重复性
np.random.seed(42)

class ExamAnxietySimulator:
    def __init__(self, n_students=100):
        self.n_students = n_students
        self.student_data = self._generate_data()

    def _generate_data(self):
        """生成模拟学生数据"""
        data = {
            'student_id': range(1, self.n_students+1),
            'gender': np.random.choice(['Male', 'Female'], size=self.n_students, p=[0.45, 0.55]),
            'major': np.random.choice(['STEM', 'Humanities'], size=self.n_students, p=[0.6, 0.4]),
            'baseline_anxiety': np.random.normal(50, 10, self.n_students).clip(20, 80)
        }

        # 生成各阶段焦虑数据
        phases = ['pre_4weeks', 'pre_1week', 'pre_24h', 'during', 'post']
        for phase in phases:
            if phase == 'pre_4weeks':
                data[phase] = data['baseline_anxiety'] * np.random.uniform(0.7, 0.9, self.n_students)
            elif phase == 'pre_1week':
                data[phase] = data['baseline_anxiety'] * np.random.uniform(0.8, 1.1, self.n_students)
            elif phase == 'pre_24h':
                data[phase] = data['baseline_anxiety'] * np.random.uniform(1.1, 1.4, self.n_students)
            elif phase == 'during':
                data[phase] = data['baseline_anxiety'] * np.random.uniform(0.8, 1.2, self.n_students)
            else:  # post
                data[phase] = data['baseline_anxiety'] * np.random.uniform(0.6, 0.95, self.n_students)

            # 添加随机噪声
            data[phase] += np.random.normal(0, 3, self.n_students)
            data[phase] = data[phase].clip(20, 100)

        # 生成生理指标
        data['hrv'] = np.random.normal(60, 15, self.n_students).clip(30, 100)
        data['eda'] = np.random.exponential(5, self.n_students).clip(1, 20)

        # 添加干预和长期追踪数据
        data['intervention'] = np.random.choice(['Mindfulness', 'Control'], size=self.n_students, p=[0.5, 0.5])
        data['cortisol_change'] = np.random.normal(-5, 10, self.n_students) * (data['intervention'] == 'Mindfulness') + np.random.normal(0, 5, self.n_students)
        data['gpa_change'] = np.random.normal(0, 0.3, self.n_students) - 0.01 * data['baseline_anxiety']

        return pd.DataFrame(data)

    def plot_anxiety_timeline(self):
        """绘制焦虑时间曲线"""
        phase_order = ['pre_4weeks', 'pre_1week', 'pre_24h', 'during', 'post']
        phase_labels = ['4 Weeks Before', '1 Week Before', '24 Hours Before', 'During Exam', 'After Exam']

        plt.figure(figsize=(12, 6))
        sns.lineplot(data=self.student_data[phase_order],
                    estimator='mean',
                    errorbar=('ci', 95),
                    linewidth=2.5)

        plt.title('Exam Anxiety Timeline (Mean ± 95% CI)', fontsize=14)
        plt.xlabel('Exam Phase', fontsize=12)
        plt.ylabel('Anxiety Score (0-100)', fontsize=12)
        plt.xticks(range(5), phase_labels, rotation=15)
        plt.ylim(20, 100)
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.show()

    def compare_majors(self):
        """比较不同专业的焦虑差异"""
        stem_data = self.student_data[self.student_data['major'] == 'STEM']
        hum_data = self.student_data[self.student_data['major'] == 'Humanities']

        print("\nMajor Comparison Results:")
        for phase in ['pre_24h', 'during']:
            t_stat, p_val = stats.ttest_ind(stem_data[phase], hum_data[phase])
            cohens_d = (stem_data[phase].mean() - hum_data[phase].mean()) / np.sqrt(
                (stem_data[phase].std()**2 + hum_data[phase].std()**2) / 2
            )
            print(f"{phase.replace('_', ' ').title()}:")
            print(f"  STEM Mean: {stem_data[phase].mean():.1f} ± {stem_data[phase].std():.1f}")
            print(f"  Humanities Mean: {hum_data[phase].mean():.1f} ± {hum_data[phase].std():.1f}")
            print(f"  t-test: t = {t_stat:.2f}, p = {p_val:.4f}")
            print(f"  Effect Size: Cohen's d = {cohens_d:.2f}\n")

    def analyze_physio_correlations(self):
        """分析生理心理相关性"""
        print("\nPhysiological-Psychological Correlations:")

        # 皮肤电反应与焦虑相关性
        corr_eda, p_eda = stats.pearsonr(
            self.student_data['eda'],
            self.student_data['during']
        )
        print(f"EDA vs During-Exam Anxiety: r = {corr_eda:.2f}, p = {p_eda:.4f}")

        # 心率变异性与焦虑相关性
        corr_hrv, p_hrv = stats.pearsonr(
            self.student_data['hrv'],
            self.student_data['during']
        )
        print(f"HRV vs During-Exam Anxiety: r = {corr_hrv:.2f}, p = {p_hrv:.4f}")

        # 绘制散点图
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        sns.regplot(x='eda', y='during', data=self.student_data, ax=ax1)
        ax1.set_title('EDA vs Exam Anxiety')
        ax1.set_xlabel('Electrodermal Activity (μS)')
        ax1.set_ylabel('Anxiety Score')

        sns.regplot(x='hrv', y='during', data=self.student_data, ax=ax2)
        ax2.set_title('HRV vs Exam Anxiety')
        ax2.set_xlabel('Heart Rate Variability (ms)')
        ax2.set_ylabel('Anxiety Score')

        plt.tight_layout()
        plt.show()

    def gender_differences(self):
        """分析性别差异"""
        male_data = self.student_data[self.student_data['gender'] == 'Male']
        female_data = self.student_data[self.student_data['gender'] == 'Female']

        print("\nGender Comparison Results:")
        for phase in ['pre_24h', 'during', 'post']:
            t_stat, p_val = stats.ttest_ind(female_data[phase], male_data[phase])
            print(f"{phase.replace('_', ' ').title()}:")
            print(f"  Female Mean: {female_data[phase].mean():.1f} ± {female_data[phase].std():.1f}")
            print(f"  Male Mean: {male_data[phase].mean():.1f} ± {male_data[phase].std():.1f}")
            print(f"  t-test: t = {t_stat:.2f}, p = {p_val:.4f}\n")

    def intervention_analysis(self):
        """分析干预效果"""
        print("\nIntervention Analysis:")
        mind_data = self.student_data[self.student_data['intervention'] == 'Mindfulness']
        control_data = self.student_data[self.student_data['intervention'] == 'Control']

        t_stat, p_val = stats.ttest_ind(mind_data['cortisol_change'], control_data['cortisol_change'])
        print(f"Cortisol Change:")
        print(f"  Mindfulness: {mind_data['cortisol_change'].mean():.1f} ± {mind_data['cortisol_change'].std():.1f}")
        print(f"  Control: {control_data['cortisol_change'].mean():.1f} ± {control_data['cortisol_change'].std():.1f}")
        print(f"  t-test: t = {t_stat:.2f}, p = {p_val:.4f}")

        # 绘制箱线图
        plt.figure(figsize=(8, 5))
        sns.boxplot(x='intervention', y='cortisol_change', data=self.student_data)
        plt.title('Cortisol Change by Intervention Group')
        plt.xlabel('Intervention Group')
        plt.ylabel('Cortisol Change (nmol/L)')
        plt.show()

    def long_term_analysis(self):
        """分析长期影响"""
        print("\nLong-term Impact Analysis:")
        model = LinearRegression()
        X = self.student_data[['baseline_anxiety']]
        y = self.student_data['gpa_change']
        model.fit(X, y)

        print(f"Regression Coefficient (β): {model.coef_[0]:.4f}")
        print(f"Intercept: {model.intercept_:.2f}")

        # 绘制回归图
        plt.figure(figsize=(8, 5))
        sns.regplot(x='baseline_anxiety', y='gpa_change', data=self.student_data)
        plt.title('Baseline Anxiety vs GPA Change')
        plt.xlabel('Baseline Anxiety Score')
        plt.ylabel('GPA Change')
        plt.show()

    def run_full_analysis(self):
        """执行完整分析流程"""
        print(f"\n{' Exam Anxiety Analysis ':=^80}")
        print(f"Sample Size: {self.n_students} students")
        print(f"Gender Distribution:\n{self.student_data['gender'].value_counts()}")
        print(f"Major Distribution:\n{self.student_data['major'].value_counts()}")

        self.plot_anxiety_timeline()
        self.compare_majors()
        self.analyze_physio_correlations()
        self.gender_differences()
        self.intervention_analysis()
        self.long_term_analysis()

# 实例化并运行分析
if __name__ == "__main__":
    simulator = ExamAnxietySimulator(n_students=150)
    simulator.run_full_analysis()