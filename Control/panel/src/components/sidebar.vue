<template>
<el-menu
  default-active="2"
  class="el-menu-vertical-demo"
    :collapse="!isCollapse"
    @open="handleOpen"
    @close="handleClose"
  >
    <el-sub-menu index="1" >
      <template #title >
        <el-icon><location /></el-icon>
        <span >学业</span>
      </template>
        <el-menu-item index="1-1" @click="gocourse">课程表</el-menu-item>
        <el-menu-item index="1-2" @click="gores">资料</el-menu-item>
        <el-menu-item index="1-3" @click="gohmwk">作业</el-menu-item>
        <!-- <el-sub-menu index="1-3" @click="goexam">子菜单</el-sub-menu> -->
        <el-menu-item index="1-4" @click="goexam">考试</el-menu-item>
    </el-sub-menu>
    <el-menu-item index="2" @click="goactvt">
      <el-icon><icon-menu /></el-icon>
      <template #title >活动管理</template>
    </el-menu-item>
    <!-- <el-menu-item index="3" @click="gonoticeer"> -->
    <el-sub-menu index="3" >
      <template #title>
      <el-icon><document /></el-icon>
        日程提醒</template>
        <el-menu-item index="3-1" @click="addnotice">添加闹钟</el-menu-item>
    </el-sub-menu>
    <el-menu-item index="4" @click="goNav">
      <el-icon><setting /></el-icon>
      <template #title >校园导航</template>
    </el-menu-item>
  </el-menu>


</template>

<script lang="ts" setup>
import { Document, Menu as IconMenu, Location,
  Setting, } from '@element-plus/icons-vue'
</script>


<script lang="ts">
import { defineComponent}from 'vue';
export default defineComponent({
  props:{ 'isCollapse':Boolean, },
  data(){
      return {
        refreshNum:1,
    }
  },
  mounted(){

  },
  methods:{
    handleOpen  (key: string, keyPath: string[]){
      console.log(key, keyPath)
      if(key=='1') this.gocourse();
      if(key=='3') this.gonoticeer();
    },
    handleClose(key: string, keyPath: string[]){
      // console.log(key, keyPath)
    },
    gocourse(){
      this.$router.push({name:"course"})
      // this.$router.push({name:'home',params: {id:'10001'}})
    },
    gores(){
      this.$router.push("/res")
    },
    gohmwk(){
      this.$router.push("/hmwk")
    },
    goexam(){
      this.$router.push("/exam")
    },
    goactvt(){
      this.$router.push("/activity")
    },
    goNav(){
      this.$router.push({name:"nav"})
    },
    gonoticeer(){
      this.$router.push({name:"notice"})
    },
    addnotice(){
      this.$router.push({name:"notice_update"})
    }
  }
})

</script>

<style lang="css">
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 600px;
}

</style>