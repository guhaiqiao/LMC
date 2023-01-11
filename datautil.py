import pandas as pd
import numpy as np
import os

repo_total = {
    'python': 120321,
    'java': 25289,
    'js': 31768
}


def get_migration(language, group=False):
    if group:
        mig_df = pd.read_csv(f'migration/{language}_migration_group.csv')
    else:
        mig_df = pd.read_csv(f'migration/{language}_migration.csv')

    mig_pattern = mig_df.value_counts(subset=['pattern'])
    mig_repo = mig_df.value_counts(subset=['repo_name'])

    mig_commit_num, mig_repo_num, mig_pattern_num = len(
        mig_df), len(mig_repo), len(mig_pattern)
    mig_repo_prop = mig_repo_num / repo_total[language] * 100
    return mig_commit_num, mig_repo_num, mig_repo_prop, mig_pattern_num


def get_year_mig(mig_df, year):
    # get migration num in year y
    return mig_df[mig_df['time_stamp'].str.contains(str(year) + '-')]


def get_year_mig_project_num(df, year):
    df = get_year_mig(df, str(year))
    if len(df) == 0:
        return 0
    return len(df.value_counts(subset=['repo_name']))


def get_year_mig_commit_num(df, year):
    df = get_year_mig(df, str(year))
    return len(df)

def get_project_num_evo(language, group=False):
    if group:
        mig_df = pd.read_csv(f'migration/{language}_migration_group.csv')
    else:
        mig_df = pd.read_csv(f'migration/{language}_migration.csv')
    project_num = []
    for year in range(2005, 2021):
        project_num.append(get_year_mig_project_num(mig_df, year))
    return project_num

def get_commit_num_evo(language, group=False):
    if group:
        mig_df = pd.read_csv(f'migration/{language}_migration_group.csv')
    else:
        mig_df = pd.read_csv(f'migration/{language}_migration.csv')
    commit_num = []
    for year in range(2005, 2021):
        commit_num.append(get_year_mig_commit_num(mig_df, year))
    return commit_num

def get_year_mig_project(df, year):
    df = get_year_mig(df, str(year))
    if len(df) == 0:
        return pd.DataFrame()
    else:
        df = df.value_counts(subset=['repo_name']).reset_index()
        df.columns = ['repo_name', 'num']
        df['year'] = year
        return df

def cal_mig_per_project(language, group=False):
    if group:
        mig_df = pd.read_csv(f'migration/{language}_migration_group.csv')
    else:
        mig_df = pd.read_csv(f'migration/{language}_migration.csv')

    year_mig_total = pd.DataFrame()
    for year in range(2005, 2021):
        year_mig = get_year_mig_project(mig_df, year)
        if len(year_mig) > 0:
            year_mig_total = pd.concat([year_mig_total, year_mig])
    mig_per_project = year_mig_total.groupby(by=['repo_name'])['num'].sum().reset_index()

    mig_per_project_per_year = []
    projects = set(year_mig_total['repo_name'].values)

    for repo in projects:
        repo_mig = year_mig_total[year_mig_total['repo_name']==repo]
        init_year = repo_mig['year'].min()
        mig_per_project_per_year.append(year_mig_total[year_mig_total['repo_name']==repo]['num'].sum() / (2022 - init_year))

    mig_per_project_per_year = pd.DataFrame(mig_per_project_per_year, columns=['num'])
    if not os.path.exists('temp'):
        os.makedirs('temp')

    if group:
        mig_per_project_per_year.to_csv(f'temp/{language}_mig_per_project_per_year_grouped.csv',index=False)
        mig_per_project.to_csv(f'temp/{language}_mig_per_project_grouped.csv',index=False)
    else:
        mig_per_project_per_year.to_csv(f'temp/{language}_mig_per_project_per_year_ungrouped.csv',index=False)
        mig_per_project.to_csv(f'temp/{language}_mig_per_project_ungrouped.csv',index=False)


def get_domain_base_df(language):
    df = pd.read_csv(f'migration/{language}_migration_group.csv')
    df = pd.DataFrame([(tup.repo_name, tup.time_stamp, tup.pattern, domain)
                       for tup in df.itertuples()
                       for domain in str(tup.domain).split('&')])
    df.columns = ['repo_name', 'time_stamp', 'pattern', 'domain']
    df = df[~df['domain'].str.contains('&')]
    domain_total = df['domain'].value_counts().reset_index()
    domain_total.columns = ['domain', 'num']
    data = np.array([domain_total['domain'].values, [0] * len(domain_total)]).T
    base_df = pd.DataFrame(data=data, columns=['domain', 'num'])
    return base_df, df

def get_year_mig_domain_dist(mig_df, year, base_df):
    # get domain distribution of migration commits in year y
    year_df = get_year_mig(mig_df, str(year))
    if len(year_df) != 0:
        domain_dist = year_df['domain'].value_counts().reset_index()
        domain_dist.columns = ['domain', 'num']
        domain_dist = pd.concat([domain_dist, base_df])
    else:
        domain_dist = base_df

    domain_dist['num'] = pd.to_numeric(domain_dist['num'])
    domain_dist = domain_dist.groupby(by=['domain'])['num'].sum().reset_index()
    domain_dist.columns = ['domain', 'num']
    domain_dist['year'] = year
    return domain_dist


def cal_domain_evo(language):
    domain_evo = pd.DataFrame()
    base_df, df = get_domain_base_df(language)
    for year in range(2005, 2021):
        domain_dist = get_year_mig_domain_dist(df, year, base_df)
        domain_evo = pd.concat([domain_evo, domain_dist])
    domain_evo.to_csv(f'temp/domain_{language}_evo_group.csv', index=False)

def get_reason_base_df(language):
    df = pd.read_csv(f'reason/{language}_reason.csv')
    df = df[df['pattern']!='tempest tempest-lib']
    reason_total = df['group_reason'].value_counts().reset_index()
    reason_total.columns = ['reason', 'num']
    data = np.array([reason_total['reason'].values, [0] * len(reason_total)]).T
    base_df = pd.DataFrame(data=data, columns=['reason', 'num'])
    return base_df, df

def get_year_mig_reason_dist(mig_df, year, base_df):
    # get reason distribution of migration commits in year y
    year_df = get_year_mig(mig_df, str(year))
    if len(year_df) != 0:
        reason_dist = year_df['group_reason'].value_counts().reset_index()
        reason_dist.columns = ['reason', 'num']
        reason_dist = pd.concat([reason_dist, base_df])
    else:
        reason_dist = base_df

    reason_dist['num'] = pd.to_numeric(reason_dist['num'])
    reason_dist = reason_dist.groupby(by=['reason'])['num'].sum().reset_index()
    reason_dist.columns = ['reason', 'num']
    reason_dist['year'] = year
    return reason_dist


def cal_reason_evo(language):
    reason_evo = pd.DataFrame()
    base_df, df = get_reason_base_df(language)
    for year in range(2005, 2021):
        reason_dist = get_year_mig_reason_dist(df, year, base_df)
        reason_evo = pd.concat([reason_evo, reason_dist])
    reason_evo.to_csv(f'temp/reason_{language}_evo.csv', index=False)
