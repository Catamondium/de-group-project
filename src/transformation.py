# import boto3
# import pandas as pd
# from io import BytesIO

# s3 = boto3.client('s3')


def lambda_handler(event, context):
    # bucket_name = event['Records'][0]['s3']['bucket']['name']
    # file_key = event['Records'][0]['s3']['object']['key']

    # read the file - return dataframe
    # df = get_df_from_parquet(file_key)

    # identify template
    # transform "2024-02-02/design.prquet" --> design

    # transform df
    # due to template
    # new_df = tables_transformation_templates[table](df)

    # save df to parquet_file
    return 0
