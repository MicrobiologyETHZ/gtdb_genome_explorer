taxa_levels = df['gtdb_taxonomy'].str.split(";", expand=True)
taxa_levels.columns = ['gtdb_domain', 'gtdb_phylum', 'gtdb_class', 'gtdb_order', 'gtdb_family', 'gtdb_genus', 'gtdb_species']
taxa_levels = taxa_levels.apply(lambda x: x.str.split("__", expand=True)[1])
st.write(taxa_levels.head())
df = pd.concat([df, taxa_levels], axis=1)
taxa_levels = df['ncbi_taxonomy'].str.split(";", expand=True)
taxa_levels.columns = ['ncbi_domain', 'ncbi_phylum', 'ncbi_class', 'ncbi_order', 'ncbi_family', 'ncbi_genus', 'ncbi_species']
taxa_levels = taxa_levels.apply(lambda x: x.str.split("__", expand=True)[1])
st.write(taxa_levels.head())
df = pd.concat([df, taxa_levels], axis=1)
df.to_csv('bac120_metadata_r207_edited.csv')