USE [Assets_OEE]
GO

/****** Object:  Table [dbo].[production_shift]    Script Date: 10/6/2026 18:48:54 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[production_shift](
	[ShiftID] [int] IDENTITY(1,1) NOT NULL,
	[EquipmentID] [int] NULL,
	[Fecha] [date] NOT NULL,
	[TiempoPlanificadoMinutos] [int] NOT NULL,
	[VelocidadIdealPorMinuto] [float] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[ShiftID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

ALTER TABLE [dbo].[production_shift]  WITH CHECK ADD FOREIGN KEY([EquipmentID])
REFERENCES [dbo].[asset_equipment] ([EquipmentID])
GO


