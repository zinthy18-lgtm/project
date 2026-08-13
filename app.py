
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Phân tích điểm GMM", page_icon="📊", layout="wide")

st.markdown("""
<style>
.stApp{background:#f5f7fb;}
div[data-testid="metric-container"]{
background:white;border-radius:12px;padding:12px;
box-shadow:0 2px 8px rgba(0,0,0,.08);}
</style>
""", unsafe_allow_html=True)

st.title("📊 HỆ THỐNG PHÂN TÍCH ĐIỂM BẤT THƯỜNG (GMM)")
uploaded=st.file_uploader("📂 Chọn file Excel",type=["xlsx","xls"])

if uploaded:
    df=pd.read_excel(uploaded)

    diem_col="CK" if "CK" in df.columns else "ĐIỂM GIỮA KỲ"
    zcol="Z_DaDinh_GMM"

    total=len(df)
    avg=df[diem_col].mean()
    low=df[df[zcol]<-2] if zcol in df.columns else pd.DataFrame()
    high=df[df[zcol]>2] if zcol in df.columns else pd.DataFrame()
    nclass=df["Lớp"].nunique() if "Lớp" in df.columns else 0
    abnormal=len(low)+len(high)

    c1,c2,c3,c4,c5,c6=st.columns(6)
    c1.metric("👨‍🎓 Tổng HS",total)
    c2.metric("📚 Số lớp",nclass)
    c3.metric("📈 Điểm TB",f"{avg:.2f}")
    c4.metric("🔴 Điểm thấp",len(low))
    c5.metric("🟢 Điểm cao",len(high))
    c6.metric("⚠️ Bất thường",abnormal)

    t1,t2,t3,t4,t5=st.tabs(["📊 Biểu đồ","📋 Tất cả","🔴 Điểm thấp","🟢 Điểm cao","🏫 Theo lớp"])

    with t1:
        fig=px.histogram(df,x=diem_col,nbins=20,title="Phổ điểm")
        st.plotly_chart(fig,use_container_width=True)
        if "Lớp" in df.columns:
            bar=df.groupby("Lớp")[diem_col].mean().reset_index()
            st.plotly_chart(px.bar(bar,x="Lớp",y=diem_col,title="Điểm trung bình theo lớp"),use_container_width=True)

    with t2:
        key=st.text_input("🔍 Tìm học sinh")
        show=df
        if key and "Họ và tên học sinh" in df.columns:
            show=df[df["Họ và tên học sinh"].astype(str).str.contains(key,case=False,na=False)]
        st.dataframe(show,use_container_width=True)

    with t3:
        st.dataframe(low,use_container_width=True)

    with t4:
        st.dataframe(high,use_container_width=True)

    with t5:
        if "Lớp" in df.columns:
            lop=st.selectbox("Chọn lớp",sorted(df["Lớp"].dropna().unique()))
            st.dataframe(df[df["Lớp"]==lop],use_container_width=True)

    with open("KetQua.xlsx","wb") as f:
        df.to_excel(f,index=False)
    with open("KetQua.xlsx","rb") as f:
        st.download_button("📥 Tải dữ liệu",f,"KetQua.xlsx")
else:
    st.info("Hãy tải file Excel để bắt đầu.")
