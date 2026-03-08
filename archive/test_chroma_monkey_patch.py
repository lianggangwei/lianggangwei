import os
import sys

# 猴子补丁：在导入chromadb之前修改sys.modules
class MockConfig:
    def __init__(self):
        self.chroma_api_impl = "chromadb.api.rust.RustBindingsAPI"
        self.chroma_server_nofile = None
        self.chroma_server_thread_pool_size = 40
        self.tenant_id = "default"
        self.topic_namespace = "default"
        self.chroma_server_host = None
        self.chroma_server_headers = None
        self.chroma_server_http_port = None
        self.chroma_server_ssl_enabled = False
        self.chroma_server_ssl_verify = None
        self.chroma_server_api_default_path = "/api/v2"
        self.chroma_server_cors_allow_origins = []
        self.chroma_http_keepalive_secs = 40.0
        self.chroma_http_max_connections = None
        self.chroma_http_max_keepalive_connections = None
        self.is_persistent = False
        self.persist_directory = "./chroma"
        self.chroma_memory_limit_bytes = 0
        self.chroma_segment_cache_policy = None
        self.allow_reset = False
        self.chroma_auth_token_transport_header = None
        self.chroma_client_auth_provider = None
        self.chroma_client_auth_credentials = None
        self.chroma_server_auth_ignore_paths = {
            "/api/v2": ["GET"],
            "/api/v2/heartbeat": ["GET"],
            "/api/v2/version": ["GET"],
            "/api/v1": ["GET"],
            "/api/v1/heartbeat": ["GET"],
            "/api/v1/version": ["GET"],
        }
        self.chroma_overwrite_singleton_tenant_database_access_from_auth = False
        self.chroma_server_authn_provider = None
        self.chroma_server_authn_credentials = None
        self.chroma_server_authn_credentials_file = None
        self.chroma_server_authz_provider = None
        self.chroma_server_authz_config = None
        self.chroma_server_authz_config_file = None
        self.chroma_product_telemetry_impl = "chromadb.telemetry.product.posthog.Posthog"
        self.chroma_telemetry_impl = self.chroma_product_telemetry_impl
        self.anonymized_telemetry = True
        self.chroma_otel_collection_endpoint = ""
        self.chroma_otel_service_name = "chromadb"
        self.chroma_otel_collection_headers = {}
        self.chroma_otel_granularity = None
        self.migrations = "apply"
        self.migrations_hash_algorithm = "md5"
        self.chroma_segment_directory_impl = "chromadb.segment.impl.distributed.segment_directory.RendezvousHashSegmentDirectory"
        self.chroma_segment_directory_routing_mode = "id"
        self.chroma_memberlist_provider_impl = "chromadb.segment.impl.distributed.segment_directory.CustomResourceMemberlistProvider"
        self.worker_memberlist_name = "query-service-memberlist"
        self.chroma_coordinator_host = "localhost"
        self.chroma_server_grpc_port = None
        self.chroma_sysdb_impl = "chromadb.db.impl.sqlite.SqliteDB"
        self.chroma_producer_impl = "chromadb.db.impl.sqlite.SqliteDB"
        self.chroma_consumer_impl = "chromadb.db.impl.sqlite.SqliteDB"
        self.chroma_segment_manager_impl = "chromadb.segment.impl.manager.local.LocalSegmentManager"
        self.chroma_executor_impl = "chromadb.execution.executor.local.LocalExecutor"
        self.chroma_query_replication_factor = 2
        self.chroma_logservice_host = "localhost"
        self.chroma_logservice_port = 50052
        self.chroma_quota_provider_impl = None
        self.chroma_rate_limiting_provider_impl = None
        self.chroma_quota_enforcer_impl = "chromadb.quota.simple_quota_enforcer.SimpleQuotaEnforcer"
        self.chroma_rate_limit_enforcer_impl = "chromadb.rate_limit.simple_rate_limit.SimpleRateLimitEnforcer"
        self.chroma_async_rate_limit_enforcer_impl = "chromadb.rate_limit.simple_rate_limit.SimpleAsyncRateLimitEnforcer"
        self.chroma_logservice_request_timeout_seconds = 3
        self.chroma_sysdb_request_timeout_seconds = 3
        self.chroma_query_request_timeout_seconds = 60
        self.chroma_db_impl = None
        self.chroma_collection_assignment_policy_impl = "chromadb.ingest.impl.simple_policy.SimpleAssignmentPolicy"
        self.environment = ""

    def __getitem__(self, key):
        return getattr(self, key)

    def require(self, key):
        val = self[key]
        if val is None:
            raise ValueError(f"Missing required config value '{key}'")
        return val

# 尝试直接导入chromadb
print("=== 测试ChromaDB基本功能（猴子补丁）===")
try:
    # 尝试导入chromadb
    import chromadb
    print("1. 测试导入:")
    print(f"ChromaDB版本: {chromadb.__version__}")
    
    # 2. 测试创建客户端
    print("\n2. 测试创建客户端:")
    client = chromadb.Client()
    print("✅ 客户端创建成功")
    
    # 3. 测试创建集合
    print("\n3. 测试创建集合:")
    collection = client.create_collection(name="test_collection")
    print("✅ 集合创建成功")
    
    # 4. 测试添加文档
    print("\n4. 测试添加文档:")
    collection.add(
        documents=["这是第一个文档", "这是第二个文档", "这是第三个文档"],
        ids=["1", "2", "3"]
    )
    print("✅ 文档添加成功")
    
    # 5. 测试查询
    print("\n5. 测试查询:")
    results = collection.query(
        query_texts=["第一个"],
        n_results=2
    )
    print("✅ 查询成功")
    print(f"查询结果: {results}")
    
    print("\n=== 测试完成 ===")
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
