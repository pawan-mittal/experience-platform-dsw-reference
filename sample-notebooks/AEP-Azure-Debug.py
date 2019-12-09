# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# !pip install --user psycopg2-binary
# !pip install --user sql_magic
import psycopg2


# %%
# Copy these settings from https://platform.adobe.com/query/configuration
connection = psycopg2.connect(
    sslmode='require',
     host='experienceplatform.platform-query.adobe.io',
     port='80',
     dbname='all',
     user='907075E95BF479EC0A495C73@AdobeOrg',
     password='eNqrVqowLVWyUsrMLY7PSzTUzU6t1DXUS04tUtJRSsxJB8oEBRuZminVAgALngwl.eNptUn9P4jAY_i770zBpu7brTC45DkFBNt0EBUKydGuHA7biVoxg_O52k-Qud9ekTd-nz_vr6fth5cK6siBxMXMYApRRFmPhODgBme0axMaJl9gJdoFNmCCJJIgw6MQHCa2Ole5yWeq4DcLTfXzI4_2O60xVhXk91LL6fiOMDIZDRAge9F3kIdDDfY_16c-eUIkcXRtyrbmWhvqxsmpZ17kqV9bVynrRel9fdbt5Udslh5e8cdipdV5epqpo4O6Z3n2D3QAFm2AaHv2pr5fF6BT0AVhez94nz8PNsvB1gJ5egpuRs5imZLEJnckjgPfXT8NouzgG0xmIZr7jb7ZHfzAA4WmLw9OyFz5Hb4viaRz1VtanKVQf97JtNzV5Y622sjQorw12LtKY2dqYU-o-P_yakvlkSJzbGerfLyZ3NOyNZj_a1XT9h_4O9cyGMWQUuJwJGyECbSwgsj2cUBvj1EEkE8jN-Fn_Sv_n_yABQkgP2ZQBbGOWZDanCbaRQ5KMgszFwDv7q9R4V7Jc8wtTd3UBqeQJTzJXwgvszMMAEeATGN4NndsejSJvHD26uE0s-XdiCrDL2sQGLlRuUOSmjOEsawbEmOVxTF_v0tf7ehyVN3NZ5vMCrtv25fs-r2Qd56XhMYpBsxpZUtWKbM4yF53zD3cqyUWsqjUv8xPXBqk7XIi8ufGdCZKpy32lNjLVUjxUShxS3Vellu_6H16ldrLu_B6_1MQ2XjHXf-tpfX4BZynyeA==.eNoBAAH__lwItdoL8MXnQWL-n8Sm74Ii_Ht61ZuGFMhhbrhv_gyEYbnqEXiMLNSQtMOLgk3GefqtMipcQ8U00N0NYz9-3Pmmf-MQ8bk5YPL-U2HFTVu24_mibSxSKKg565-UhQZI9pYMddlPZnXKlrbhwtOXzutP89oPW0Qy48Gr8HU25XHRm03HTBTTlIfD5KPdEpWOwPE2t9oDlNcMeFOWrv6vElUAgifdwf5UbdI72dpFHyrjUAuDWOC9kO00gG6AtSWQ8bolMHCsvrlzbCrMwFlt-ZFzYXcCrDkYhXwz-6z43yiTUeS2F0skcvXCkTSuqhUbapfkGoEqU1aAyfA-4EuR9biWsonq')


# %%
import pandas
df = pandas.read_sql(('show tables'), con=connection)
print (df)
df.head()


# %%



# %%


