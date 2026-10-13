# Is Sheep Box Plugin Registry

Is Sheep Box 插件市场索引仓库。

- `plugins.json`：全量插件索引（格式见 IsSheepBox 主仓库 `docs/plugin-registry-schema.md`）
- `schemas/plugins.schema.json`：draft-07 JSON Schema（机器校验用）

## 维护流程

### 新增插件上架

1. 插件开发者在自己的 GitHub 仓库准备好 Release 与 zip 包。
2. 向本仓库提交 PR，在 `plugins.json` 数组追加条目。
3. 维护者审核：manifest 合规性（下载 zip 校验）、权限合理性、ID 唯一性、`downloadUrl` 可访问。
4. 合并后更新 `generatedAt` 字段。

### 插件更新版本

1. 插件作者发布新的 GitHub Release。
2. 提交 PR 修改 `plugins.json` 对应条目：`version`、`downloadUrl`、`releaseUrl`、`publishedAt`、`permissions`（如有变化）。
3. 维护者审核合并。

### 插件下架

- 删除数组中对应条目即可；已安装用户不受影响，只是市场不再展示新安装入口。

## 客户端消费

宿主客户端拉取 `https://raw.githubusercontent.com/PastSheep/issheepbox-registry/main/plugins.json`，校验 `registryVersion` 兼容后按 `plugins[]` 渲染市场列表。
