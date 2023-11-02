FROM mcr.microsoft.com/dotnet/sdk:6.0
WORKDIR /app
COPY *.csproj ./
RUN dotnet restore
COPY . ./
RUN dotnet add package Npgsql
RUN dotnet add package Confluent.Kafka
RUN dotnet build
CMD ["dotnet", "run"]

