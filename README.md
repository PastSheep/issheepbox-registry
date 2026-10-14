# Is Sheep Box Plugin Registry

Is Sheep Box 插件市场索引仓库。

- `plugins.json`：全量插件索引（格式见 IsSheepBox 主仓库 `docs/plugin-registry-schema.md`）
- `schemas/plugins.schema.json`：draft-07 JSON Schema（机器校验用）

## 上架状态（pending）

当前索引中 4 个第一方插件均以 `status: "pending"` 占位登记，而非直接上架为 `active`。

### 为什么先 pending 而不是 active

`active` 状态要求 `downloadUrl` 指向一个可直接 GET 下载的 zip 资产（GitHub Release assets），且 `releaseUrl` 指向对应 Release 页面。当前 4 个插件**均未发布过任何 zip 资产**，发布流水线（per-plugin 打包出 zip、产出 Release）尚未跑通。为保持索引诚实、不伪造 URL，先登记元数据为 `pending`，而不是写一个不存在的下载地址。

### pending 的语义

- 元数据已登记：`id` / `name` / `description` / `author` / `version` / `apiVersion` / `permissions` / `repository` 等字段齐备并通过 schema 校验。
- zip 资产待发布：`releaseUrl` / `downloadUrl` 缺省。
- **客户端不应为 pending 条目提供安装入口**——没有可下载的 zip，渲染市场列表时应隐藏「安装」按钮或标记为「即将上架」。

### pending → active 的流转条件

1. 发布流水线跑通，为每个插件产出 per-plugin zip 资产并发布 GitHub Release（TASK-011）。
2. 在对应条目补齐 `releaseUrl`、`downloadUrl`，并将 `status` 置为 `"active"`。
3. 将 `publishedAt` 从「登记时间占位」更新为该版本实际 Release 时间。
4. 更新顶层 `generatedAt`。

### 为什么不上架 approval-policy / market-client

- **approval-policy**：第一方基础设施插件，随应用内置分发。公开上架会与内置副本产生冲突与版本分裂（同一 ID 既有内置副本又有市场安装副本）。
- **market-client**：不是插件，是客户端库包（无 `plugin.json` manifest），不满足插件条目要求，不进入市场索引。

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
