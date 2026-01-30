-- CreateTable
CREATE TABLE "Student_Table" (
    "id" SERIAL NOT NULL,
    "first_name" TEXT NOT NULL,
    "last_name" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "phone_number" TEXT,
    "dob" TIMESTAMP(3),
    "gender" TEXT,
    "country" TEXT,
    "city" TEXT,
    "bio" TEXT,
    "profile_image" TEXT,
    "future_goal" TEXT,
    "password" TEXT NOT NULL,
    "account_status" TEXT NOT NULL DEFAULT 'active',
    "email_verified" BOOLEAN NOT NULL DEFAULT false,
    "last_login" TIMESTAMP(3),
    "password_last_change" TIMESTAMP(3),
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Student_Table_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Instructor_Table" (
    "instructor_id" SERIAL NOT NULL,
    "first_name" TEXT NOT NULL,
    "last_name" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "phone_number" TEXT,
    "gender" TEXT,
    "dob" TIMESTAMP(3),
    "bio" TEXT,
    "profile_image" TEXT,
    "city" TEXT,
    "country" TEXT,
    "account_type" TEXT,
    "account_status" TEXT NOT NULL DEFAULT 'active',
    "qualification" TEXT,
    "expertise_area" TEXT,
    "year_of_experience" INTEGER,
    "email_verified" BOOLEAN NOT NULL DEFAULT false,
    "last_login" TIMESTAMP(3),
    "password_last_change" TIMESTAMP(3),
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Instructor_Table_pkey" PRIMARY KEY ("instructor_id")
);

-- CreateTable
CREATE TABLE "Admin_Table" (
    "admin_id" SERIAL NOT NULL,
    "first_name" TEXT NOT NULL,
    "last_name" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "phone_number" TEXT,
    "profile_image" TEXT,
    "account_status" TEXT NOT NULL DEFAULT 'active',
    "email_verified" BOOLEAN NOT NULL DEFAULT false,
    "last_login" TIMESTAMP(3),
    "password_last_change" TIMESTAMP(3),
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Admin_Table_pkey" PRIMARY KEY ("admin_id")
);

-- CreateTable
CREATE TABLE "Course_Table" (
    "course_id" SERIAL NOT NULL,
    "course_title" TEXT NOT NULL,
    "course_description" TEXT,
    "course_thumbnail" TEXT,
    "course_level" TEXT,
    "course_language" TEXT,
    "meta_title" TEXT,
    "meta_description" TEXT,
    "meta_keywords" TEXT,
    "estimated_comp_time" INTEGER,
    "course_duration" INTEGER,
    "total_modules" INTEGER NOT NULL DEFAULT 0,
    "total_lectures" INTEGER NOT NULL DEFAULT 0,
    "total_videos" INTEGER NOT NULL DEFAULT 0,
    "total_resources" INTEGER NOT NULL DEFAULT 0,
    "course_status" TEXT NOT NULL DEFAULT 'draft',
    "published_at" TIMESTAMP(3),
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Course_Table_pkey" PRIMARY KEY ("course_id")
);

-- CreateTable
CREATE TABLE "Invoice_Table" (
    "invoice_id" SERIAL NOT NULL,
    "invoice_type" TEXT,
    "invoice_status" TEXT,
    "invoice_method" TEXT,
    "invoice_gateway" TEXT,
    "transaction_id" TEXT,
    "gateway_transaction_id" TEXT,
    "invoice_amount" DOUBLE PRECISION NOT NULL,
    "tax_amount" DOUBLE PRECISION DEFAULT 0,
    "total_amount" DOUBLE PRECISION NOT NULL,
    "discount_applied" DOUBLE PRECISION DEFAULT 0,
    "discount_code" TEXT,
    "platform_commission" DOUBLE PRECISION DEFAULT 0,
    "instructor_share" DOUBLE PRECISION DEFAULT 0,
    "currency_type" TEXT,
    "billing_cycle" TEXT,
    "next_billing_date" TIMESTAMP(3),
    "card_type" TEXT,
    "card_last_four_digit" TEXT,
    "device_info" TEXT,
    "ip_address" TEXT,
    "is_successful" BOOLEAN NOT NULL DEFAULT false,
    "failure_reason" TEXT,
    "deleted_at" TIMESTAMP(3),
    "receipt_sent" BOOLEAN NOT NULL DEFAULT false,
    "receipt_sent_email" TEXT,
    "receipt_sent_date" TIMESTAMP(3),
    "receipt_url" TEXT,
    "instructor_payout_status" TEXT,
    "instructor_payout_date" TIMESTAMP(3),
    "invoice_date" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "invoice_completed_at" TIMESTAMP(3),
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Invoice_Table_pkey" PRIMARY KEY ("invoice_id")
);

-- CreateTable
CREATE TABLE "Resume_Table" (
    "resume_id" SERIAL NOT NULL,
    "resume_title" TEXT NOT NULL,
    "resume_template" TEXT,
    "resume_file_path" TEXT,
    "file_url" TEXT,
    "resume_format" TEXT,
    "file_size" INTEGER,
    "total_pages" INTEGER,
    "template_style" TEXT,
    "font_style" TEXT,
    "color_schema" TEXT,
    "layout_style" TEXT,
    "generation_status" TEXT,
    "generation_date" TIMESTAMP(3),
    "resume_version" INTEGER DEFAULT 1,
    "resume_score" DOUBLE PRECISION,
    "resume_status" TEXT NOT NULL DEFAULT 'active',
    "deleted_at" TIMESTAMP(3),
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Resume_Table_pkey" PRIMARY KEY ("resume_id")
);

-- CreateTable
CREATE TABLE "Company_Table" (
    "company_id" SERIAL NOT NULL,
    "company_name" TEXT NOT NULL,
    "company_email" TEXT NOT NULL,
    "company_password" TEXT NOT NULL,
    "phone_number" TEXT,
    "company_logo" TEXT,
    "company_website" TEXT,
    "company_description" TEXT,
    "company_location" TEXT,
    "city" TEXT,
    "country" TEXT,
    "company_type" TEXT,
    "industry_type" TEXT,
    "company_size" TEXT,
    "vision_statement" TEXT,
    "account_type" TEXT,
    "account_status" TEXT NOT NULL DEFAULT 'active',
    "reg_number" TEXT,
    "reg_date" TIMESTAMP(3),
    "invitation_limit" INTEGER DEFAULT 0,
    "pending_invitation" INTEGER DEFAULT 0,
    "total_invited" INTEGER NOT NULL DEFAULT 0,
    "active_student" INTEGER NOT NULL DEFAULT 0,
    "completed_student" INTEGER NOT NULL DEFAULT 0,
    "active_course" INTEGER NOT NULL DEFAULT 0,
    "completed_course" INTEGER NOT NULL DEFAULT 0,
    "total_course_requested" INTEGER NOT NULL DEFAULT 0,
    "subscription_plan" TEXT,
    "subscription_status" TEXT,
    "subscription_start_at" TIMESTAMP(3),
    "subscription_end_at" TIMESTAMP(3),
    "last_login" TIMESTAMP(3),
    "password_last_change" TIMESTAMP(3),
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Company_Table_pkey" PRIMARY KEY ("company_id")
);

-- CreateTable
CREATE TABLE "Roadmap_Table" (
    "roadmap_id" SERIAL NOT NULL,
    "roadmap_title" TEXT NOT NULL,
    "roadmap_description" TEXT,
    "roadmap_status" TEXT,
    "course_in_progress" INTEGER DEFAULT 0,
    "course_completed" INTEGER DEFAULT 0,
    "completion_per" DOUBLE PRECISION DEFAULT 0,
    "total_course" INTEGER DEFAULT 0,
    "mandatory_course" INTEGER DEFAULT 0,
    "optional_course" INTEGER DEFAULT 0,
    "prequisite_course" INTEGER DEFAULT 0,
    "course_sequence" TEXT,
    "difficulty_level" TEXT,
    "estimated_duration" INTEGER,
    "total_section" INTEGER DEFAULT 0,
    "total_learning_hour" INTEGER DEFAULT 0,
    "start_at" TIMESTAMP(3),
    "expected_comp_date" TIMESTAMP(3),
    "generation_date" TIMESTAMP(3),
    "last_activity_date" TIMESTAMP(3),
    "last_ai_adjustment_date" TIMESTAMP(3),
    "deleted_at" TIMESTAMP(3),
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Roadmap_Table_pkey" PRIMARY KEY ("roadmap_id")
);

-- CreateTable
CREATE TABLE "CourseCategory_Table" (
    "category_id" SERIAL NOT NULL,
    "category_name" TEXT NOT NULL,
    "category_description" TEXT,
    "is_parent_category" BOOLEAN NOT NULL DEFAULT false,
    "is_sub_category" BOOLEAN NOT NULL DEFAULT false,
    "has_sub_category" BOOLEAN NOT NULL DEFAULT false,
    "category_level" INTEGER DEFAULT 0,
    "category_path" TEXT,
    "sub_category_name" TEXT,
    "sub_category_description" TEXT,
    "sub_category_count" INTEGER DEFAULT 0,
    "beginner_course" INTEGER DEFAULT 0,
    "intermediate_course" INTEGER DEFAULT 0,
    "advance_course" INTEGER DEFAULT 0,
    "category_icon" TEXT,
    "category_thumbnail" TEXT,
    "category_color" TEXT,
    "meta_title" TEXT,
    "meta_description" TEXT,
    "meta_keywords" TEXT,
    "tags" TEXT,
    "last_course_add" TIMESTAMP(3),
    "correct_answer" INTEGER DEFAULT 0,
    "published_at" TIMESTAMP(3),
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "CourseCategory_Table_pkey" PRIMARY KEY ("category_id")
);

-- CreateIndex
CREATE UNIQUE INDEX "Student_Table_email_key" ON "Student_Table"("email");

-- CreateIndex
CREATE UNIQUE INDEX "Instructor_Table_email_key" ON "Instructor_Table"("email");

-- CreateIndex
CREATE UNIQUE INDEX "Admin_Table_email_key" ON "Admin_Table"("email");

-- CreateIndex
CREATE UNIQUE INDEX "Company_Table_company_email_key" ON "Company_Table"("company_email");
