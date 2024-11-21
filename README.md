#端末情報ファイルの構成
　xmlsファイル

 注意：
　ヘッダーに「端末番号」と「設置場所」を含むこと
　OPE_TIMEのformatは「yyyy/mm/dd h:mm」であること
 
　![image](https://github.com/user-attachments/assets/e5ed88e2-b027-495e-818a-f082c7ecc370)

#アクセスログ(複数同時取り込み可能)
  csvファイル
　OPE_TIME	OPE_DATE	JOB_CODE	SHOKUKBN_NAME	KA_NAME	PID	U_ID	U_NAME	WS_ID	FCD	Value2　...
　
  注意：
  　ヘッダーに「OPE_TIME」と「FCD」を含むこと
  　OPE_TIMEのformatは「yyyy/mm/dd h:mm」であること
 
![image](https://github.com/user-attachments/assets/1a9176a0-8778-42b4-b5e5-92334236edf3)
