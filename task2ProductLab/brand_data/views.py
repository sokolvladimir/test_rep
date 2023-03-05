import json

import aiohttp
import asyncio
from asgiref.sync import async_to_sync
import pandas as pd

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .pydantic_models import CardModel, ExcelData
from .serializers import FileOrNumberSerializer


class HomePageView(APIView):
    serializer_class = FileOrNumberSerializer

    @async_to_sync
    async def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data.get('file'):
                try:
                    list_articles = self.check_excel_file(serializer.validated_data.get('file'))
                    result = await self.handle_articles(list_articles.numbers)
                except ValueError as ex:
                    return Response({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)
            else:
                result = await self.handle_articles([serializer.validated_data.get('number')])
                result = result[0]

            result = json.dumps(result)

            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def check_excel_file(file_path: str) -> ExcelData:
        df = pd.read_excel(file_path, usecols=[0], header=None)
        data = {'numbers': df[0].tolist()}
        return ExcelData(**data)

    async def handle_articles(self, list_sku: list[int]):
        return await self.get_data(list_sku)

    @staticmethod
    async def get_x_info_v2() -> str | None:
        async with aiohttp.ClientSession() as session:
            headers = {'x-requested-with': 'XMLHttpRequest'}
            async with session.post('https://www.wildberries.ru/webapi/user/get-xinfo-v2', headers=headers) as response:
                result = await response.json()
                return result['xinfo']

    @staticmethod
    async def get_info(sku: int, x_info: str) -> json:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://card.wb.ru/cards/detail?{x_info}&nm={sku}') as response:
                try:
                    result = await response.text()
                    card = CardModel.parse_raw(result)

                    return card.data.products[0].dict()
                except Exception as ex:
                    return json.dumps({"article": sku, "brand": None, "title": None, "error": str(ex)})

    async def get_data(self, list_sku: list):
        x_info = await self.get_x_info_v2()
        data_list = []
        async with asyncio.TaskGroup() as tg:
            for sku in list_sku:
                data_list.append(await tg.create_task(self.get_info(sku, x_info)))
        return data_list
