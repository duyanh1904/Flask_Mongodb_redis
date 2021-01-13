from src.app.Model.CodeModel import CodeModel


from src.app.helper.GeneratorCode import GeneratorCodes


class routeController():

    def getMID(self, code, merchantId):
        return CodeModel(code, merchantId).getCode()

    def addMID(self, merchantId):
        genCode = GeneratorCodes(9).generator()
        return CodeModel(genCode, merchantId).addCode()

    def updateMID(self, code, merchantId):
        return CodeModel(code, merchantId).updateCode()

    def deleteMID(self, code, merchantId):
        return CodeModel(code, merchantId).deleteCode()

    def cacheMID(self, code, merchantId):
        return CodeModel(code, merchantId).CacheCode()











