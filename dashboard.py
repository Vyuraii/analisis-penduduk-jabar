import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Konfigurasi Halaman
st.set_page_config(
    page_title="Analisis Kependudukan Jawa Barat",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Animasi CSS untuk Judul Bergerak (Gradient Text)
st.markdown("""
<style>
@keyframes gradient {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
.animated-title {
    background: linear-gradient(-45deg, #FF512F, #DD2476, #1A2980, #26D0CE);
    background-size: 400% 400%;
    animation: gradient 5s ease infinite;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 42px;
    font-weight: 900;
    margin-bottom: 10px;
}
.subtitle {
    color: #555555;
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    return df

df = load_data()

# Sidebar: Logo Jawa Barat di Kiri Atas
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Logo_of_West_Java_Province.svg/512px-Logo_of_West_Java_Province.svg.png", 
    use_container_width=True
)
st.sidebar.title("Filter Data")
st.sidebar.divider()

tahun_options = sorted(df['tahun'].unique())
tahun_filter = st.sidebar.multiselect(
    "Pilih Tahun:",
    options=tahun_options,
    default=tahun_options
)

kabkota_options = sorted(df['kabupaten_kota'].unique())
kabkota_filter = st.sidebar.multiselect(
    "Pilih Kabupaten/Kota:",
    options=kabkota_options,
    default=kabkota_options
)

st.sidebar.divider()
st.sidebar.markdown(
    "**Sumber Data:**\n\n"
    "Open Data Jawa Barat, Dinas Kependudukan dan Pencatatan Sipil\n\n"
    "Periode: 2019 hingga 2020"
)

# Filter Data
df_filtered = df[
    (df['tahun'].isin(tahun_filter)) &
    (df['kabupaten_kota'].isin(kabkota_filter))
]

# Header dengan Animasi CSS
st.markdown('<div class="animated-title">Dashboard Analisis Kependudukan Jawa Barat</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Analisis Pertumbuhan Penduduk dan Rasio Jenis Kelamin per Kabupaten/Kota (2019 hingga 2020)</div>', unsafe_allow_html=True)
st.divider()

# KPI Metrics
col1, col2, col3, col4 = st.columns(4)

total_pop = df_filtered['jumlah_penduduk'].sum()
total_lk  = df_filtered[df_filtered['jenis_kelamin']=='LAKI-LAKI']['jumlah_penduduk'].sum()
total_pr  = df_filtered[df_filtered['jenis_kelamin']=='PEREMPUAN']['jumlah_penduduk'].sum()

with col1:
    st.metric("Total Penduduk", f"{total_pop:,.0f}")
with col2:
    st.metric("Total Laki-laki", f"{total_lk:,.0f}")
with col3:
    st.metric("Total Perempuan", f"{total_pr:,.0f}")
with col4:
    sex_ratio_overall = (total_lk / total_pr * 100) if total_pr > 0 else 0
    st.metric("Sex Ratio", f"{sex_ratio_overall:.1f}")

st.divider()

# Pertanyaan 1: Pertumbuhan Penduduk
st.header("Pertanyaan 1: Pertumbuhan Penduduk per Kabupaten/Kota")
st.info("Menganalisis kabupaten/kota yang mengalami pertumbuhan jumlah penduduk tertinggi dan terendah di Provinsi Jawa Barat dari tahun 2019 ke tahun 2020.", icon=None)

# Persiapan Data Pertumbuhan
pop_kabkota = df[df['kabupaten_kota'].isin(kabkota_filter)].groupby(
    ['kabupaten_kota', 'tahun'])['jumlah_penduduk'].sum().reset_index()
pop_pivot = pop_kabkota.pivot(
    index='kabupaten_kota', columns='tahun', values='jumlah_penduduk').reset_index()

if 2019 in pop_pivot.columns and 2020 in pop_pivot.columns:
    pop_pivot.columns = ['kabupaten_kota', 'pop_2019', 'pop_2020']
    pop_pivot['pertumbuhan_persen'] = ((pop_pivot['pop_2020'] - pop_pivot['pop_2019']) / pop_pivot['pop_2019'] * 100).round(2)
    pop_pivot['pertumbuhan_absolut'] = pop_pivot['pop_2020'] - pop_pivot['pop_2019']
    pop_pivot_sorted = pop_pivot.sort_values('pertumbuhan_persen', ascending=True) # Ascending for Plotly horizontal bar
else:
    pop_pivot_sorted = pop_pivot.copy()

tab1, tab2 = st.tabs(["Visualisasi Animasi", "Tabel Data"])

with tab1:
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        if 'pertumbuhan_persen' in pop_pivot_sorted.columns:
            fig1 = px.bar(
                pop_pivot_sorted, 
                x='pertumbuhan_persen', 
                y='kabupaten_kota', 
                orientation='h',
                color='pertumbuhan_persen',
                color_continuous_scale='Turbo',
                title="Persentase Pertumbuhan Penduduk (%)",
                labels={'pertumbuhan_persen': 'Pertumbuhan (%)', 'kabupaten_kota': 'Kabupaten/Kota'}
            )
            fig1.update_layout(margin=dict(l=0, r=0, t=40, b=0), title_font=dict(size=16, color='black'))
            st.plotly_chart(fig1, use_container_width=True)

    with col_chart2:
        if 'pop_2020' in pop_pivot_sorted.columns:
            top10 = pop_pivot_sorted.nlargest(10, 'pop_2020').sort_values('pop_2020', ascending=True)
            fig2 = go.Figure()
            if 'pop_2019' in top10.columns:
                fig2.add_trace(go.Bar(
                    y=top10['kabupaten_kota'], x=top10['pop_2019'], 
                    name='2019', orientation='h', marker_color='#A0E3F5'
                ))
            fig2.add_trace(go.Bar(
                y=top10['kabupaten_kota'], x=top10['pop_2020'], 
                name='2020', orientation='h', marker_color='#1A2980'
            ))
            fig2.update_layout(
                barmode='group', 
                title="10 Kabupaten/Kota Terpopuler (2020)",
                margin=dict(l=0, r=0, t=40, b=0),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig2, use_container_width=True)

with tab2:
    if 'pertumbuhan_persen' in pop_pivot_sorted.columns:
        display_df = pop_pivot_sorted.sort_values('pertumbuhan_persen', ascending=False).copy()
        display_df = display_df[['kabupaten_kota','pop_2019','pop_2020','pertumbuhan_absolut','pertumbuhan_persen']]
        display_df.columns = ['Kabupaten/Kota','Penduduk 2019','Penduduk 2020','Pertambahan','Pertumbuhan (%)']
        st.dataframe(display_df.style.format({
            'Penduduk 2019': '{:,.0f}',
            'Penduduk 2020': '{:,.0f}',
            'Pertambahan': '{:,.0f}',
            'Pertumbuhan (%)': '{:.2f}%'
        }), use_container_width=True)

st.divider()

# Pertanyaan 2: Sex Ratio
st.header("Pertanyaan 2: Distribusi Sex Ratio per Kabupaten/Kota (2020)")
st.info("Memetakan distribusi rasio jenis kelamin penduduk di setiap kabupaten/kota Jawa Barat pada tahun 2020.", icon=None)

pop_2020_data = df[(df['tahun'] == 2020) & (df['kabupaten_kota'].isin(kabkota_filter))]
if not pop_2020_data.empty:
    sex_pivot = pop_2020_data.groupby(['kabupaten_kota', 'jenis_kelamin'])['jumlah_penduduk'].sum().unstack()
    if 'LAKI-LAKI' in sex_pivot.columns and 'PEREMPUAN' in sex_pivot.columns:
        sex_pivot.columns = ['laki_laki', 'perempuan']
        sex_pivot['sex_ratio'] = (sex_pivot['laki_laki'] / sex_pivot['perempuan'] * 100).round(2)
        sex_pivot['total'] = sex_pivot['laki_laki'] + sex_pivot['perempuan']
        sex_pivot = sex_pivot.reset_index().sort_values('sex_ratio', ascending=True)

        tab3, tab4 = st.tabs(["Visualisasi Animasi", "Tabel Data"])

        with tab3:
            col_chart3, col_chart4 = st.columns(2)
            
            with col_chart3:
                fig3 = px.bar(
                    sex_pivot, 
                    x='sex_ratio', 
                    y='kabupaten_kota', 
                    orientation='h',
                    color='sex_ratio',
                    color_continuous_scale='Plasma',
                    title="Sex Ratio per Kabupaten/Kota",
                    labels={'sex_ratio': 'Sex Ratio (Laki-laki per 100 Perempuan)', 'kabupaten_kota': 'Kabupaten/Kota'}
                )
                fig3.add_vline(x=100, line_dash="dash", line_color="black", annotation_text="Seimbang (100)")
                fig3.update_layout(margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig3, use_container_width=True)

            with col_chart4:
                fig4 = go.Figure()
                fig4.add_trace(go.Bar(
                    x=sex_pivot['kabupaten_kota'], y=sex_pivot['laki_laki'], 
                    name='Laki-laki', marker_color='#23a6d5'
                ))
                fig4.add_trace(go.Bar(
                    x=sex_pivot['kabupaten_kota'], y=sex_pivot['perempuan'], 
                    name='Perempuan', marker_color='#e73c7e'
                ))
                fig4.update_layout(
                    barmode='stack', 
                    title="Komposisi Penduduk Laki-laki dan Perempuan",
                    margin=dict(l=0, r=0, t=40, b=0),
                    xaxis_tickangle=-45,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig4, use_container_width=True)

        with tab4:
            display_sex = sex_pivot.sort_values('sex_ratio', ascending=False).copy()
            display_sex = display_sex[['kabupaten_kota', 'laki_laki', 'perempuan', 'sex_ratio', 'total']]
            display_sex.columns = ['Kabupaten/Kota', 'Laki-laki', 'Perempuan', 'Sex Ratio', 'Total']
            st.dataframe(display_sex.style.format({
                'Laki-laki': '{:,.0f}',
                'Perempuan': '{:,.0f}',
                'Total': '{:,.0f}',
                'Sex Ratio': '{:.2f}'
            }), use_container_width=True)

st.divider()

# Analisis Lanjutan: Clustering
st.header("Analisis Lanjutan: Clustering Kabupaten/Kota")
st.markdown("Pengelompokan otomatis menggunakan gelembung animasi interaktif berdasarkan **Pertumbuhan Penduduk** dan **Sex Ratio**.")

if 'pertumbuhan_persen' in pop_pivot_sorted.columns and not pop_2020_data.empty:
    cluster_df = pop_pivot_sorted.merge(
        sex_pivot[['kabupaten_kota', 'sex_ratio', 'total']], on='kabupaten_kota', how='inner'
    )
    if not cluster_df.empty:
        cluster_df['Kategori Pertumbuhan'] = pd.cut(
            cluster_df['pertumbuhan_persen'],
            bins=[-float('inf'), 0, 5, 10, float('inf')],
            labels=['Menurun atau Stagnan', 'Rendah (0 hingga 5%)', 'Sedang (5 hingga 10%)', 'Tinggi (Lebih dari 10%)']
        )
        cluster_df['Kategori Sex Ratio'] = pd.cut(
            cluster_df['sex_ratio'],
            bins=[0, 98, 102, float('inf')],
            labels=['Dominasi Perempuan', 'Seimbang', 'Dominasi Laki-laki']
        )

        col_a, col_b = st.columns(2)
        with col_a:
            fig5 = px.scatter(
                cluster_df,
                x="pertumbuhan_persen",
                y="sex_ratio",
                size="total",
                color="pertumbuhan_persen",
                hover_name="kabupaten_kota",
                color_continuous_scale="Spectral",
                size_max=40,
                title="Gelembung Distribusi Pertumbuhan Berbanding Sex Ratio",
                labels={"pertumbuhan_persen": "Pertumbuhan (%)", "sex_ratio": "Sex Ratio"}
            )
            fig5.add_hline(y=100, line_dash="dash", line_color="gray")
            st.plotly_chart(fig5, use_container_width=True)

        with col_b:
            pivot_cat = pd.crosstab(cluster_df['Kategori Pertumbuhan'], cluster_df['Kategori Sex Ratio'])
            fig6 = px.density_heatmap(
                cluster_df, 
                x='Kategori Sex Ratio', 
                y='Kategori Pertumbuhan',
                color_continuous_scale="Viridis",
                text_auto=True,
                title="Peta Panas (Heatmap) Distribusi Cluster"
            )
            st.plotly_chart(fig6, use_container_width=True)

st.divider()

# Kesimpulan
st.header("Kesimpulan dan Rekomendasi")

col_c1, col_c2 = st.columns(2)
with col_c1:
    st.subheader("Kesimpulan 1: Pertumbuhan Penduduk")
    st.info(
        "Terdapat ketimpangan pertumbuhan yang signifikan antar kabupaten/kota. "
        "Wilayah penyangga industri seperti Karawang, Bekasi, dan Purwakarta mengalami "
        "pertumbuhan tertinggi karena daya tarik lapangan kerja. Sementara kota-kota besar "
        "seperti Bandung mengalami suburbanisasi, di mana penduduk bergerak ke pinggiran kota.",
        icon=None
    )

with col_c2:
    st.subheader("Kesimpulan 2: Rasio Jenis Kelamin")
    st.info(
        "Sex ratio Jawa Barat secara keseluruhan mendekati seimbang (sekitar 103), namun "
        "kabupaten kawasan industri cenderung memiliki sex ratio lebih tinggi "
        "akibat migrasi tenaga kerja laki-laki. Tidak ada kabupaten/kota dengan "
        "ketidakseimbangan yang ekstrem.",
        icon=None
    )

st.subheader("Rekomendasi Tindakan Lanjutan")
st.success(
    "1. Memprioritaskan investasi infrastruktur seperti perumahan, transportasi, sekolah, dan fasilitas kesehatan "
    "di kabupaten dengan pertumbuhan penduduk tertinggi.\n\n"
    "2. Merancang program berbasis gender di kabupaten dengan sex ratio tinggi, "
    "khususnya perlindungan pekerja migran dan pemberdayaan perempuan di kawasan industri.\n\n"
    "3. Mengevaluasi kebijakan tata kota di kota-kota dengan penurunan penduduk untuk memahami "
    "penyebab suburbanisasi dan menyusun program revitalisasi pusat kota.\n\n"
    "4. Membangun sistem pemantauan kependudukan berbasis data yang diperbarui secara tahunan "
    "untuk mendukung pengambilan keputusan berbasis bukti.",
    icon=None
)

st.divider()
st.caption("Dashboard dibuat untuk Proyek Analisis Data. Sumber Data: Open Data Jabar, Disdukcapil Jawa Barat.")

# Animasi ekstra dari Streamlit saat load
st.balloons()