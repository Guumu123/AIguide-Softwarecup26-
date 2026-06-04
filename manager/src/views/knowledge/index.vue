<template>
  <div class="knowledge-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>景区知识库管理</span>
          <el-button type="primary" icon="Plus" @click="handleAdd">上传文档</el-button>
        </div>
      </template>

      <el-form :inline="true" :model="queryForm" class="demo-form-inline">
        <el-form-item label="文档名称">
          <el-input v-model="queryForm.name" placeholder="请输入文档名称" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="queryForm.status" placeholder="请选择状态" style="width: 120px">
            <el-option label="全部" value="" />
            <el-option label="已处理" value="processed" />
            <el-option label="处理中" value="processing" />
            <el-option label="失败" value="failed" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleQuery">查询</el-button>
          <el-button @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="tableData" style="width: 100%" v-loading="loading">
        <el-table-column prop="name" label="文档名称" />
        <el-table-column prop="type" label="类型" width="100">
          <template #default="scope">
            <el-tag>{{ scope.row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="size" label="大小" width="100" />
        <el-table-column prop="status" label="分块状态" width="120">
          <template #default="scope">
            <el-tag :type="statusType(scope.row.status)">{{ statusText(scope.row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="updateTime" label="更新时间" width="180" />
        <el-table-column label="操作" width="250">
          <template #default="scope">
            <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="small" type="success" @click="handleReindex(scope.row)">重新索引</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination mt-20">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 上传对话框 -->
    <el-dialog v-model="dialogVisible" title="上传文档" width="500px">
      <el-upload
        class="upload-demo"
        drag
        action="/api/admin/knowledge/upload"
        multiple
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          拖拽文件到此处 或 <em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            支持 Markdown/Word/Excel 格式，单个文件不超过 10MB
          </div>
        </template>
      </el-upload>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="dialogVisible = false">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessageBox, ElMessage } from 'element-plus'

const loading = ref(false)
const dialogVisible = ref(false)
const queryForm = reactive({
  name: '',
  status: ''
})

const tableData = ref([
  { id: 1, name: '灵山大佛讲解词.md', type: 'Markdown', size: '25KB', status: 'processed', updateTime: '2024-05-20 10:00:00' },
  { id: 2, name: '景区FAQ手册.xlsx', type: 'Excel', size: '1.2MB', status: 'processed', updateTime: '2024-05-19 15:30:00' },
  { id: 3, name: '梵宫艺术背景资料.docx', type: 'Word', size: '5.6MB', status: 'processing', updateTime: '2024-05-20 11:15:00' },
  { id: 4, name: '九龙灌浴表演时间表.md', type: 'Markdown', size: '5KB', status: 'failed', updateTime: '2024-05-18 09:00:00' }
])

const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(4)

const statusType = (status: string) => {
  const map: Record<string, string> = {
    processed: 'success',
    processing: 'warning',
    failed: 'danger'
  }
  return map[status] || 'info'
}

const statusText = (status: string) => {
  const map: Record<string, string> = {
    processed: '已处理',
    processing: '处理中',
    failed: '失败'
  }
  return map[status] || '未知'
}

const handleAdd = () => {
  dialogVisible.value = true
}

const handleQuery = () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
  }, 500)
}

const resetQuery = () => {
  queryForm.name = ''
  queryForm.status = ''
}

const handleEdit = (row: any) => {
  ElMessage.info(`编辑文档: ${row.name}`)
}

const handleReindex = (row: any) => {
  ElMessageBox.confirm(`确认重新触发 BGE-M3 Embedding 索引?`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    ElMessage.success('已触发重新索引')
  })
}

const handleDelete = (row: any) => {
  ElMessageBox.confirm(`确认删除文档 ${row.name}?`, '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'danger'
  }).then(() => {
    ElMessage.success('删除成功')
  })
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
}
</script>

<style scoped lang="scss">
.pagination {
  display: flex;
  justify-content: flex-end;
}
</style>
