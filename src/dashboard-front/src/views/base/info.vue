<template>
  <div class="app-content">
    <bk-alert v-if="!curApigw.statusBoolean" type="warning" class="warning-alert" :title="$t('当前网关已停用，如需使用，请先启用')"></bk-alert>
    <section class="apigw-card top-editing mb17">
      <div class="logo-wrapper">
        <span :class="['logo', curApigw.statusBoolean ? '' : 'disabled']">{{ curApigw.name[0] && curApigw.name[0].toUpperCase() }}</span>
      </div>
      <div class="left-info">
        <div>
          <span :class="['name', 'mr5', curApigw.statusBoolean ? '' : 'disabled']">{{ curApigw.name }}</span>
          <span v-if="curApigw.is_official" class="apigw-tag mr5"> {{ $t('官方') }} </span>
          <span v-if="curApigw.hosting_type === 1" class="apigw-tag warning mr5" v-bk-tooltips="$t('该网关使用专享实例托管资源')"> {{ $t('专享') }} </span>
          <span :class="['apigw-tag', curApigw.statusBoolean ? 'success' : 'disabled']">
            <i class="apigateway-icon icon-ag-minus-circle" v-if="!curApigw.statusBoolean"></i>
            {{ curApigw.statusBoolean ? $t('启用中') : $t('已停用') }}
          </span>
        </div>
        <div class="apigw-item mb15">
          <div class="item-label"> {{ $t('简介') }}： </div>
          <div class="item-value">
            <template v-if="!isEdit.description">
              {{curApigw.description || '--'}}
              <i class="apigateway-icon icon-ag-edit-line icon-hover ml4" @click="handleEdit('description')" v-bk-clickoutside="handleClickOutSide"></i>
            </template>
            <bk-input
              v-else
              ref="description"
              v-model="curApigw.description"
              style="width: 560px;"
              @blur="handleBlur('description')"
              @enter="handleBlur('description', 'enter')"
            ></bk-input>
          </div>
        </div>
        <div class="operate">
          <bk-button theme="default" class="mr5" style="width: 88px;" @click="editApigw"> {{ $t('编辑') }} </bk-button>
          <template v-if="curApigw.status">
            <bk-button theme="default" class="mr5 stop-btn" style="width: 88px;" @click="toggleApigwStatus"> {{ $t('停用') }} </bk-button>
          </template>
          <template v-else>
            <bk-button theme="primary" class="mr5" style="width: 88px;" @click="toggleApigwStatus"> {{ $t('立即启用') }} </bk-button>
          </template>
          <template v-if="curApigw.statusBoolean">
            <bk-popover :content="$t('请先停用才可删除')">
              <bk-button theme="default" class="mr5" style="width: 88px;" :disabled="curApigw.statusBoolean"> {{ $t('删除') }} </bk-button>
            </bk-popover>
          </template>
          <template v-else>
            <bk-button theme="default" class="mr5" style="width: 88px;" @click="removeApigw"> {{ $t('删除') }} </bk-button>
          </template>
        </div>
      </div>
    </section>

    <section class="apigw-card base-info">
      <p class="apigw-title">{{ $t('基本信息') }}</p>

      <!-- 基本信息 -->
      <div class="apigw-form-item">
        <div class="item-label">
          {{ $t('是否公开') }}：
        </div>
        <div class="item-value">
          <bk-switcher v-model="curApigw.is_public" theme="primary" @change="handlePublicChange"></bk-switcher>
        </div>
      </div>

      <div class="apigw-form-item">
        <div class="item-label">
          {{ $t('访问域名') }}：
        </div>
        <div class="item-value">
          {{curApigw.domain}}
          <i class="apigateway-icon icon-ag-copy ml10 copy-btn icon-hover" @click="handleCopy(curApigw.domain)"></i>
          <!-- <a :href="curApigw.domain" target="_blank"><i class="apigateway-icon icon-ag-jump ml5"></i></a> -->
        </div>
      </div>

      <div class="apigw-form-item">
        <div class="item-label">
          {{ $t('文档地址') }}：
        </div>
        <div class="item-value">
          <template v-if="curApigw.is_public">
            {{curApigw.docs_url}}
            <i class="apigateway-icon icon-ag-copy ml10 copy-btn icon-hover" @click="handleCopy(curApigw.docs_url)"></i>
            <!-- <a :href="curApigw.docs_url" target="_blank"><i class="apigateway-icon icon-ag-jump ml5"></i></a> -->
          </template>
          <template v-else>
            <span style="color: #dcdee5;"> {{ $t('网关未公开，不提供在线 API 文档') }} </span>
          </template>
        </div>
      </div>

      <div class="apigw-form-item">
        <div class="item-label">
          {{ $t('维护人员') }}：
        </div>
        <div class="item-value">
          <template v-if="!isEdit.maintainers">
            <bk-popover placement="right">
              <p class="ag-field-text" style="max-width: 200px; margin-top: -3px;">{{curApigw.maintainers.join('; ')}}</p>
              <div slot="content" style="white-space: normal; max-width: 300px;">
                {{curApigw.maintainers.join('; ')}}
              </div>
            </bk-popover>
            <i class="apigateway-icon icon-ag-edit-line icon-hover ml4" @click="handleEdit('maintainers')"></i>
          </template>
          <user
            v-else
            ref="maintainers"
            v-model="curApigw.maintainers"
            style="width: 560px;"
            @blur="handleBlur('maintainers')"
          ></user>
        </div>
      </div>

      <div class="apigw-form-item">
        <div class="item-label">
          {{ $t('创建人') }}：
        </div>
        <div class="item-value">
          <div class="ag-form-content">{{curApigw.created_by || '--'}}</div>
        </div>
      </div>

      <div class="apigw-form-item">
        <div class="item-label">
          {{ $t('创建时间') }}：
        </div>
        <div class="item-value">
          <div class="ag-form-content">{{curApigw.created_time || '--'}}</div>
        </div>
      </div>

      <p class="apigw-title mt40"> {{ $t('API公钥(指纹)') }} </p>

      <div class="apigw-form-item">
        <div class="item-label"></div>
        <div class="item-value">
          <div class="ag-key-value">
            <div class="key">
              <i class="apigateway-icon icon-ag-lock-fill1"></i>
            </div>
            <div class="value">
              <span class="f14">{{curApigw.public_key_fingerprint}}</span>
              <span>
                <i class="apigateway-icon icon-ag-download icon-hover fr ml10" @click="download"></i>
                <i class="apigateway-icon icon-ag-copy copy-btn icon-hover fr" @click="handleCopy(curApigw.public_key)"></i>
              </span>
            </div>
          </div>
          <p class="ag-tip mt8">
            <i class="apigateway-icon icon-ag-info"></i>
            {{ $t('可用于解密传入后端接口的请求头 X-Bkapi-JWT') }}，
            <a :href="GLOBAL_CONFIG.DOC.JWT" target="_blank" class="ag-primary"> {{ $t('更多详情') }} </a>
          </p>
        </div>
      </div>
    </section>

    <bk-dialog
      v-model="delApigwDialog.visiable"
      width="540"
      :title="$t(`确认删除网关【{name}】？`, { name: curApigw.name })"
      :theme="'primary'"
      :header-position="'left'"
      :mask-close="false"
      :loading="delApigwDialog.isLoading">
      <div class="ps-form">
        <div class="form-tips" v-html="delTips"></div>
        <div class="mt15">
          <bk-input v-model="formRemoveConfirmApigw"></bk-input>
        </div>
      </div>
      <template slot="footer">
        <bk-button
          theme="primary"
          :disabled="!formRemoveApigw"
          @click="deleteApigw">
          {{ $t('确定') }}
        </bk-button>
        <bk-button
          theme="default"
          @click="delApigwDialog.visiable = false">
          {{ $t('取消') }}
        </bk-button>
      </template>
    </bk-dialog>

    <create-apigw
      :visible="isEditApigw"
      :apigw-id="curApigw.id"
      @close="isEditApigw = false"
      @refresh="reload"
    />
  </div>
</template>

<script>
  import { catchErrorHandler } from '@/common/util'
  import { bus } from '@/common/bus'
  import createApigw from '@/views/base/create-apigw'
  import User from '@/components/user'

  export default {
    components: {
      createApigw,
      User
    },
    data () {
      return {
        isPageLoading: true,
        curApigw: {
          name: '',
          description: '',
          status: 0,
          statusBoolean: false,
          statusForFe: false,
          is_public: true,
          maintainers: [],
          maintainersForFe: []
        },
        delApigwDialog: {
          visiable: false,
          isLoading: false
        },
        formRemoveConfirmApigw: '',
        isEditApigw: false,
        isEdit: {
          description: false,
          maintainers: false
        },
        isUpdate: false
      }
    },
    computed: {
      formRemoveApigw () {
        return this.curApigw.name === this.formRemoveConfirmApigw
      },
      delTips () {
        return this.$t(`请完整输入 <code class="gateway-del-tips">{name}</code> 来确认删除网关！`, { name: this.curApigw.name })
      }
    },
    created () {
      this.init()
    },
    methods: {
      init () {
        this.getApigwDetail()
      },

      async getApigwDetail () {
        const apigwId = this.$route.params.id

        try {
          const res = await this.$store.dispatch('apis/getApisDetail', apigwId)
          this.curApigw = res.data
          this.curApigw.statusBoolean = Boolean(this.curApigw.status)
        } catch (e) {
          catchErrorHandler(e, this)
        } finally {
          this.isPageLoading = false
          this.$store.commit('setMainContentLoading', false)
        }
      },

      editApigw () {
        this.isEditApigw = true
      },

      reload () {
        // 刷新当前组件
        bus.$emit('update-component')
      },

      download () {
        const content = this.curApigw.public_key

        const elment = document.createElement('a')
        const blob = new Blob([content], {
          type: 'text/plain'
        })
        elment.download = `bk_apigw_public_key_${this.curApigw.name}.pub`
        elment.href = URL.createObjectURL(blob)
        elment.click()
        URL.revokeObjectURL(blob)
      },

      toggleApigwStatus () {
        const self = this
        let title = this.$t('确认要启用网关？')
        let subTitle = ''
        if (this.curApigw.status) {
          title = this.$t('确认是否停用网关？')
          subTitle = this.$t('网关停用后，网关下所有资源不可访问，请确认是否继续操作？')
        }

        this.$bkInfo({
          title: title,
          subTitle: subTitle,
          confirmFn () {
            self.changeApigwStatus()
          }
        })
      },

      removeApigw () {
        this.delApigwDialog.visiable = true
        this.formRemoveConfirmApigw = ''
      },

      async changeApigwStatus () {
        const apigwId = this.$route.params.id
        const status = this.curApigw.status === 1 ? 0 : 1
        try {
          await this.$store.dispatch('apis/toggleApisStatus', { apigwId, data: { status } })
          this.curApigw.status = status
          this.curApigw.statusBoolean = Boolean(status)
          this.$bkMessage({
            theme: 'success',
            message: this.$t('更新成功')
          })
          this.$store.commit('updateCurApigw', this.curApigw)
        } catch (e) {
          catchErrorHandler(e, this)
        } finally {
          this.isPageLoading = false
          this.$store.commit('setMainContentLoading', false)
        }
      },

      async deleteApigw () {
        const apigwId = this.$route.params.id
        try {
          await this.$store.dispatch('apis/deleteApis', { apigwId, status })
          this.$bkMessage({
            theme: 'success',
            message: this.$t('删除成功')
          })
          this.$router.push({
            name: 'index'
          })
        } catch (e) {
          catchErrorHandler(e, this)
        } finally {
          this.isPageLoading = false
          this.$store.commit('setMainContentLoading', false)
        }
      },

      handleCopy (text) {
        this.$copyText(text).then((e) => {
          this.$bkMessage({
            theme: 'success',
            limit: 1,
            message: this.$t('复制成功')
          })
        }, () => {
          this.$bkMessage({
            theme: 'error',
            limit: 1,
            message: this.$t('复制失败')
          })
        })
      },

      handleEdit (key) {
        this.isEdit[key] = !this.isEdit[key]
        this.isUpdate = true
        this.$nextTick(() => {
          this.$refs[key].focus()
        })
      },

      handleBlur (key, eventName) {
        if (this.isEdit[key]) {
          this.isEdit[key] = false
          eventName && this.updateApigw()
        }
      },

      handlePublicChange () {
        this.updateApigw()
      },

      handleClickOutSide (mousedownEvent, mouseupEvent, el) {
        const classList = Array.from(mousedownEvent.target.classList)
        // 过滤icon点击响应
        if (classList.includes('icon-ag-edit-line')) {
          return false
        }
        if (this.isUpdate) {
          this.updateApigw()
          this.isUpdate = false
        }
      },

      // 更新基本信息
      async updateApigw () {
        const apigwId = this.$route.params.id
        try {
          const params = {
            apigwId,
            data: this.curApigw
          }
          params.data.status = Number(this.curApigw.statusBoolean)

          await this.$store.dispatch('apis/updateApis', params)
          // 编辑成功，重新获取基本信息
          this.$bkMessage({
            theme: 'success',
            message: this.$t('更新成功！')
          })
        } catch (e) {
          catchErrorHandler(e, this)
        } finally {
          this.getApigwDetail()
        }
      }
    }
  }
</script>

<style lang="postcss" scoped>
    @import '@/css/variable.css';

    .ag-dl {
        padding: 15px 40px 5px 30px;
    }

    .ag-user-type {
        width: 560px;
        height: 80px;
        background: #FAFBFD;
        border-radius: 2px;
        border: 1px solid #DCDEE5;
        padding: 17px 20px 0 20px;
        position: relative;
        overflow: hidden;

        .apigateway-icon {
            font-size: 80px;
            position: absolute;
            color: #ECF2FC;
            top: 15px;
            right: 20px;
            z-index: 0;
        }

        strong {
            font-size: 14px;
            margin-bottom: 10px;
            line-height: 1;
            display: block;
        }

        p {
            font-size: 12px;
            color: #63656E;
        }
    }
    .stop-btn {
        &:hover {
            background: $dangerColor;
            border-color: $dangerColor;
            color: #FFF;
        }
    }
    .ps-form {
        font-size: 14px;
        .form-tips code {
            color: #c7254e;
            padding: 3px 4px;
            margin: 0;
            background-color: rgba(0, 0, 0, 0.04);
            border-radius: 3px;
        }
    }
    .status-dot {
        padding: 2px 10px;
        font-size: 12px;
        border-radius: 2px;
        background: #F0F1F5;
        color: #63656E;
    }
    .status-dot.success {
        background: #E4FAF0;
        color: #14A568;
    }
    .is-public {
        color: #FF9C01;
    }
    .warning-alert {
        margin-bottom: 16px;
    }

    .top-editing {
        display: flex;
        width: 100%;
        .logo {
            width: 80px;
            height: 80px;
            text-align: center;
            line-height: 80px;
            background: #F0F5FF;
            color: #3A84FF;
            font-size: 40px;
            font-weight: bold;
            border-radius: 8px;
            display: inline-block;
            margin-right: 20px;
            vertical-align: middle;
            margin-left: 14px;
            &.disabled {
                color: #C4C6CC;
                background: #F0F1F5;
            }
        }
        .left-info {
            padding-top: 16px;
            width: 50%;
            .name {
                font-size: 16px;
                color: #313238;
                font-weight: 700;
                &.disabled {
                    color: #63656E;
                }
            }
        }
    }
    .apigw-form-item {
        font-size: 12px;
        display: flex;
        align-items: center;
        line-height: 32px;
        margin-bottom: 8px;
        .item-label {
            width: 158px;
            text-align: right;
            color: #63656E;
        }
        .item-value {
            flex: 1;
            margin-right: 300px;
            color: #313238;
        }
    }
</style>
<style>
    .gateway-del-tips {
        color: #c7254e;
        padding: 3px 4px;
        margin: 0;
        background-color: rgba(0, 0, 0, 0.04);
        border-radius: 3px;
    }

    .ag-form-info .bk-grid-row .bk-grid-col:last-child {
      padding-left: 0 !important;
    }
</style>
