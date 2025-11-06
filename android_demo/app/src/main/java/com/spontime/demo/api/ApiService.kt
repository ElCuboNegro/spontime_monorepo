package com.spontime.demo.api

import retrofit2.Response
import retrofit2.http.*

interface ApiService {

    // Authentication endpoints
    @POST("auth/register/")
    suspend fun register(@Body request: RegisterRequest): Response<AuthResponse>

    @POST("auth/login/")
    suspend fun login(@Body request: LoginRequest): Response<AuthResponse>

    @POST("auth/logout/")
    suspend fun logout(): Response<Map<String, String>>

    @GET("auth/profile/")
    suspend fun getProfile(): Response<User>

    // Plans endpoints
    @GET("plans/")
    suspend fun getPlans(@Query("page") page: Int = 1): Response<PaginatedResponse<Plan>>

    @GET("plans/{id}/")
    suspend fun getPlan(@Path("id") id: String): Response<Plan>

    @POST("plans/")
    suspend fun createPlan(@Body request: CreatePlanRequest): Response<Plan>

    // Users endpoints
    @GET("users/")
    suspend fun getUsers(@Query("page") page: Int = 1): Response<PaginatedResponse<User>>

    @GET("users/{id}/")
    suspend fun getUser(@Path("id") id: String): Response<User>

    // Messages endpoints
    @GET("messages/")
    suspend fun getMessages(
        @Query("plan_id") planId: String? = null,
        @Query("page") page: Int = 1
    ): Response<PaginatedResponse<Message>>
}
