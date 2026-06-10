USE [Assets_OEE]
GO

/****** Object:  Table [dbo].[oee_raw_data]    Script Date: 10/6/2026 18:48:35 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[oee_raw_data](
	[RawDataID] [int] IDENTITY(1,1) NOT NULL,
	[ShiftID] [int] NULL,
	[FechaRegistro] [datetime] NULL DEFAULT (getdate()),
	[TiempoParadaMinutos] [int] NOT NULL,
	[TotalProducido] [int] NOT NULL,
	[TotalDefectuosos] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[RawDataID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

ALTER TABLE [dbo].[oee_raw_data]  WITH CHECK ADD FOREIGN KEY([ShiftID])
REFERENCES [dbo].[production_shift] ([ShiftID])
GO


