<template>
  <div class="avatar-container">
    <el-row :gutter="20">
      <el-col :span="16">
        <el-card header="方案配置">
          <el-form :model="form" label-width="120px">
            <el-form-item label="方案名称">
              <el-input v-model="form.name" placeholder="如: 禅意主题" />
            </el-form-item>

            <el-form-item label="服装主题">
              <el-radio-group v-model="form.costume_theme">
                <el-radio-button label="zen">禅意</el-radio-button>
                <el-radio-button label="buddhist">佛教</el-radio-button>
                <el-radio-button label="modern">现代</el-radio-button>
              </el-radio-group>
            </el-form-item>

            <el-form-item label="声音音色">
              <el-select v-model="form.voice_type">
                <el-option label="温暖女声" value="warm_female" />
                <el-option label="沉稳男声" value="calm_male" />
                <el-option label="童声" value="child" />
              </el-select>
            </el-form-item>

            <el-form-item label="语速调节">
              <el-slider v-model="form.voice_speed" :min="0.8" :max="1.2" :step="0.1" show-stops />
            </el-form-item>

            <el-form-item label="UI主题">
              <el-color-picker v-model="form.ui_theme" :predefine="predefineColors" />
            </el-form-item>

            <el-form-item label="讲解风格">
              <el-radio-group v-model="form.speech_style">
                <el-radio-button label="academic">学术严谨</el-radio-button>
                <el-radio-button label="story">轻松故事</el-radio-button>
                <el-radio-button label="family">亲子互动</el-radio-button>
              </el-radio-group>
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="savePreset">保存方案</el-button>
              <el-button @click="preview">实时预览</el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <el-card header="方案列表" class="mt-20">
          <el-table :data="presets" style="width: 100%">
            <el-table-column prop="name" label="方案名称" />
            <el-table-column prop="costume_theme" label="服装" />
            <el-table-column prop="voice_type" label="音色" />
            <el-table-column prop="speech_style" label="风格" />
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button size="small" @click="editPreset(scope.row)">编辑</el-button>
                <el-button size="small" type="danger" @click="deletePreset(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card header="效果预览">
          <div class="preview-window">
            <div class="avatar-placeholder">
              <el-icon :size="100" color="#909399"><User /></el-icon>
              <p>Live2D 实时预览区域</p>
              <p style="font-size: 12px; color: #999;">(此处将嵌入渲染引擎)</p>
            </div>
            <div class="preview-info" :style="{ borderTop: '4px solid ' + form.ui_theme }">
              <div class="preview-bubble">
                您好，我是您的 AI 向导。当前讲解风格为：{{ speechStyleName }}
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { ElMessage } from 'element-plus'

const form = reactive({
  name: '默认方案',
  costume_theme: 'zen',
  voice_type: 'warm_female',
  voice_speed: 1.0,
  ui_theme: '#409EFF',
  speech_style: 'story'
})

const predefineColors = ref([
  '#409EFF',
  '#67C23A',
  '#E6A23C',
  '#F56C6C',
  '#909399',
  '#009688',
  '#FF9800'
])

const presets = ref([
  { name: '默认方案', costume_theme: 'zen', voice_type: 'warm_female', speech_style: 'story' },
  { name: '学术讲解', costume_theme: 'modern', voice_type: 'calm_male', speech_style: 'academic' },
  { name: '亲子导游', costume_theme: 'zen', voice_type: 'child', speech_style: 'family' }
])

const speechStyleName = computed(() => {
  const map: any = {
    academic: '学术严谨',
    story: '轻松故事',
    family: '亲子互动'
  }
  return map[form.speech_style]
})

const savePreset = () => {
  ElMessage.success('方案保存成功')
}

const preview = () => {
  ElMessage.info('正在加载实时预览...')
}

const editPreset = (row: any) => {
  Object.assign(form, row)
}

const deletePreset = (row: any) => {
  ElMessage.warning(`已删除方案: ${row.name}`)
}
</script>

<style scoped lang="scss">
.preview-window {
  height: 500px;
  background-color: #f8f9fa;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  .avatar-placeholder {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: #909399;
  }
  .preview-info {
    padding: 20px;
    background: #fff;
    .preview-bubble {
      background: #f0f2f5;
      padding: 15px;
      border-radius: 8px;
      position: relative;
      &::after {
        content: '';
        position: absolute;
        top: -10px;
        left: 20px;
        border-width: 0 10px 10px;
        border-style: solid;
        border-color: transparent transparent #f0f2f5;
      }
    }
  }
}
</style>
