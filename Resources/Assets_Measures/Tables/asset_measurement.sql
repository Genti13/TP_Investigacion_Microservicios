USE [Assets_Measures]
GO

/****** Object:  Table [dbo].[asset_measurement]    Script Date: 10/6/2026 18:45:21 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[asset_measurement](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ValorDecimal] [decimal](18, 2) NOT NULL,
	[FechaRegistro] [datetime2](7) NOT NULL DEFAULT (getdate()),
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO


