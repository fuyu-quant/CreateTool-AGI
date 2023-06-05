from setuptools import setup, find_packages


setup(
    name='createtoolagi',
    version='0.2.1',
    packages=find_packages(),  # ここでパッケージ内のモジュールが自動的に見つけられます
    install_requires=[  # 依存関係リスト
        'langchain==0.0.167',
        'openai==0.27.4',
        'tiktoken==0.4.0',
        'qdrant-client==1.2.0',
        # 他に必要なパッケージがあればここに追加
    ],
    description="createtoolagi",
    author='fuyu-quant',  
    license='MIT'
)